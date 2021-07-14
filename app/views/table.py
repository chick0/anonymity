
from flask import Blueprint
from flask import render_template


bp = Blueprint(
    name="table",
    import_name="table",
    url_prefix="/table"
)


@bp.route("")
def show_all_table():
    # TODO: show all table using ul
    return "TO-DO"


@bp.route("/<string:name>")
def show_table(name: str):
    # TODO: show all boards
    return "TO-DO"
