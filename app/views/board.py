
from flask import Blueprint
from flask import request
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
    ).paginate(page=request.args.get("page", 1, type=int))

    return render_template(
        "board/show_all.html",
        board_list=board
    )
