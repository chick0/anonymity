
from flask import Blueprint
from flask import request
from flask import render_template
from flask import url_for

from app import db
from app import redis
from app.ip import get_ip_hash
from app.models import Token
from app.models import Board


bp = Blueprint(
    name="admin",
    import_name="admin",
    url_prefix="/admin"
)


@bp.route("/verify")
def verify():
    # TODO: verify with one-time token
    # TODO: delete one-time token and create access token [TIME LIMIT: 30m]  (<ip>:<rand string>)
    # TODO: create session with redis [DO NOT USE COOKIE/SESSION]
    return "TO-DO"


@bp.route("/write")
def write():
    # TODO: verify with access token
    # TODO: write notice
    return "TO-DO"


@bp.route("")
def show_all():
    board = Board.query.filter_by(
        is_notice=True
    ).order_by(
        Board.idx.desc()
    ).paginate(page=request.args.get("page", 1, type=int),
               max_per_page=8)

    prev_page = url_for(".show_all", page=board.prev_num) \
        if board.prev_num is not None else "javascript:alert('page not found')"

    next_page = url_for(".show_all", page=board.next_num) \
        if board.next_num is not None else "javascript:alert('page not found')"

    return render_template(
        "board/show_all.html",
        board_list=board,
        prev=prev_page,
        next=next_page
    )
