from datetime import datetime
from datetime import timedelta

from flask import Blueprint

from app import db
from app.models import Salt
from app.models import Board
from app.models import Recommend
from app.ip import gen_salt


bp = Blueprint(
    name="cron",
    import_name="cron",
    url_prefix="/cron"
)


@bp.route("")
def run():
    # 1) check the ip salt
    salt = Salt.query.first()
    if salt is None:
        gen_salt()
    else:
        if salt.created > datetime.now() + timedelta(days=1):
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

    return "OK"
