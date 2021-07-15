
from flask import Blueprint
from flask import request
from flask import render_template
from flask import url_for

from app.models import Table
from app.models import Board


bp = Blueprint(
    name="table",
    import_name="table",
    url_prefix="/table"
)


@bp.route("")
def show_all_table():
    tables = Table.query.all()
    return render_template(
        "table/show_all_table.html",
        tables=tables
    )


@bp.route("/<string:name>")
def show_table(name: str):
    board = Board.query.filter_by(
        table_name=name
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
