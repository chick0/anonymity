
from flask import Blueprint
from flask import request
from flask import url_for
from flask import render_template

from app.models import Board


bp = Blueprint(
    name="board",
    import_name="board",
    url_prefix="/"
)


@bp.route("")
def show_all():
    board = Board.query.order_by(
        Board.idx.desc()
    ).paginate(page=request.args.get("page", 1, type=int),
               max_per_page=8)

    prev_page = url_for("board.show_all", page=board.prev_num) \
        if board.prev_num is not None else "javascript:alert('page not found')"

    next_page = url_for("board.show_all", page=board.next_num) \
        if board.next_num is not None else "javascript:alert('page not found')"

    return render_template(
        "board/show_all.html",
        board_list=board,
        prev=prev_page,
        next=next_page
    )
