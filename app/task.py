from time import time
from time import sleep
from datetime import datetime
from datetime import timedelta
from threading import Thread

from app import db
from app.models import Salt
from app.models import Board
from app.models import Token
from app.models import Recommend
from app.ip import gen_salt


def core(app):
    task_list = [
        {
            "time": time(),
            "target": salt_lifetime,   # 2h
            "call": 2 * 60 * 60
        },
        {
            "time": time(),
            "target": vote_updater,    # 2m
            "call": 2 * 60
        },
        {
            "time": time(),
            "target": token_cleaner,   # 5m
            "call": 5 * 60
        },
    ]

    while True:
        now = time()
        for target_id, task_target in enumerate(task_list):
            time_flow = int(now - task_target['time'])

            if time_flow >= task_target['call']:
                Thread(
                    target=task_target['target'],
                    args=(app,)
                ).start()

                # timer reset
                task_list[target_id]['time'] = now

        sleep(30)


def salt_lifetime(app):
    with app.app_context():
        salt = Salt.query.first()
        if salt is None:
            gen_salt()
        else:
            if datetime.now() >= salt.created + timedelta(days=1):
                db.session.delete(salt)
                gen_salt()


def vote_updater(app):
    with app.app_context():
        board_cache = {}
        votes = Recommend.query.filter_by(
            is_board=True,
            used=False
        ).limit(200).all()
        for vote in votes:
            board = board_cache.get(vote.target_idx, None)
            if board is None:
                board = Board.query.filter_by(
                    idx=vote.target_idx
                ).first()
                board_cache[vote.target_idx] = board

            if board is not None:
                if vote.vote is True:
                    board.good += 1
                else:
                    board.bad += 1

                # save vote result
                vote.used = True
            else:
                # if the target is empty, delete the vote result
                db.session.delete(vote)

        db.session.commit()


def token_cleaner(app):
    with app.app_context():
        for token in Token.query.all():
            if not token.expire >= datetime.now():
                db.session.delete(token)

        db.session.commit()
