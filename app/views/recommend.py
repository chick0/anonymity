
from flask import Blueprint
from flask import request
from flask import jsonify

from app import db
from app.models import Board
from app.models import Recommend
from app.ip import get_ip_hash

bp = Blueprint(
    name="recommend",
    import_name="recommend",
    url_prefix="/recommend"
)


@bp.route("/ip")
def ip():
    return get_ip_hash()


@bp.route("/board", methods=['GET', 'POST'])
def board():
    idx = request.args.get("idx", default=-1, type=int)

    if request.method == "GET":
        board_ = Board.query.filter_by(
            idx=idx
        ).first()
        return jsonify({
            "idx": idx,
            "good": board_.good,
            "bad": board_.bad,
        })
    elif request.method == "POST":
        vote = Recommend.query.filter_by(
            target_idx=idx,
            is_board=True,
            ip=get_ip_hash()
        ).first()

        if vote is None:
            vote = Recommend()
            vote.target_idx = idx
            vote.is_board = True
            vote.vote = True if request.form.get("vote", type=str) == 'good' else False
            vote.used = False
            vote.ip = get_ip_hash()

            db.session.add(vote)
            db.session.commit()
        else:
            return jsonify({
                "result": "canceled",
                "message": "already voted"
            }), 400

        return jsonify({
            "idx": idx,
            "vote": vote.vote,
            "result": "ok",
            "date": vote.date.__str__()
        })
