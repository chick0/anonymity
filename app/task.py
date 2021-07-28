from time import sleep
from datetime import datetime
from datetime import timedelta

from app import db
from app.models import Salt
from app.models import Board
from app.models import Token
from app.models import Recommend
from app.ip import gen_salt


def loop(app) -> None:
    while True:
        with app.app_context():
            # 1) check the ip salt
            salt = Salt.query.first()
            if salt is None:
                gen_salt()
            else:
                if datetime.now() >= salt.created + timedelta(days=1):
                    db.session.delete(salt)
                    db.session.commit()
                    gen_salt()

            # 2) Collect Voting Results
            # 2-1) Board
            votes = Recommend.query.filter_by(
                is_board=True,
                used=False
            ).all()
            for vote in votes:
                board = Board.query.filter_by(
                    idx=vote.target_idx
                ).first()
                if board is not None:
                    if vote.vote is True:
                        board.good += 1
                    else:
                        board.bad += 1

                    vote.used = True
                else:
                    db.session.delete(vote)

            db.session.commit()

            # 3) Remove Expired Sessions
            for token in Token.query.all():
                if not token.expire >= datetime.now():
                    db.session.delete(token)
            db.session.commit()

        sleep(35)
