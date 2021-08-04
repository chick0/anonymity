
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import Response
from flask_babel import gettext

from app import db
from app.models import Board
from app.models import Recommend
from app.ip import get_ip_hash

bp = Blueprint(
    name="recommend",
    import_name="recommend",
    url_prefix="/recommend"
)


@bp.get("/ip")
def ip():
    return Response(
        mimetype="text/plain",
        response=f"Your IP Hash is {get_ip_hash()}"
    )


@bp.get("/board")
def board():
    board_obj = Board.query.filter_by(
        idx=request.args.get("idx", default=-1, type=int)
    ).first()
    if board_obj is None:
        return jsonify({
            "error": gettext("target_not_found")
        })

    return jsonify({
        "idx": board_obj.idx,
        "good": board_obj.good,
        "bad": board_obj.bad,
    })


@bp.post("/board")
def board_post():
    board_obj = Board.query.filter_by(
        idx=request.args.get("idx", default=-1, type=int)
    ).first()
    if board_obj is None:
        return jsonify({
            "error": gettext("target_not_found")
        })

    vote = Recommend.query.filter_by(
        target_idx=board_obj.idx,
        is_board=True,
        ip=get_ip_hash()
    ).first()

    if vote is None:
        vote = Recommend()
        vote.target_idx = board_obj.idx
        vote.is_board = True
        vote.vote = True if request.form.get("vote", type=str) == 'good' else False
        vote.used = False
        vote.ip = get_ip_hash()

        db.session.add(vote)
        db.session.commit()
    else:
        return jsonify({
            "result": "canceled",
            "message": gettext("already_vote")
        }), 400

    return jsonify({
        "idx": board_obj.idx,
        "vote": vote.vote,
        "result": "ok",
        "date": vote.date.__str__()
    })
