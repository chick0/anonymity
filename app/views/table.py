from uuid import uuid4

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask_babel import gettext

from app import redis
from app.ip import get_ip_hash
from app.models import Table
from app.models import Board


bp = Blueprint(
    name="table",
    import_name="table",
    url_prefix="/table"
)


@bp.get("")
def show_all_table():
    tables = Table.query.all()
    return render_template(
        "table/show_all_table.html",
        tables=tables
    )


@bp.get("/<string:name>")
def show_table(name: str):
    if name == "admin":
        return redirect(url_for("admin.show_all"))

    table = Table.query.filter_by(
        name=name
    ).first()
    if table is None:
        return redirect(url_for(".show_all_table"))

    board = Board.query.filter_by(
        table_name=name
    ).paginate(page=request.args.get("page", 1, type=int),
               max_per_page=8)

    page_not_found = gettext("page_not_found")

    prev_page = url_for(".show_all", page=board.prev_num) \
        if board.prev_num is not None else f"javascript:alert('{page_not_found}')"

    next_page = url_for(".show_all", page=board.next_num) \
        if board.next_num is not None else f"javascript:alert('{page_not_found}')"

    return render_template(
        "board/show_all.html",
        board_list=board,
        prev=prev_page,
        next=next_page,

        write_url=url_for("table.write", name=table.name)
    )


@bp.get("/<string:name>/write")
def write(name: str):
    if name == "admin":
        return redirect(url_for("admin.write"))

    table = Table.query.filter_by(
        name=name
    ).first()
    if table is None:
        return redirect(url_for(".show_all_table"))

    table_key = uuid4().__str__()
    redis.set(f"{get_ip_hash()}:{table_key}", name, ex=3600)

    return redirect(url_for("write.write", table_key=table_key))
