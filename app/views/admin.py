
from flask import Blueprint
from flask import request
from flask import render_template

from app import db
from app import redis
from app.ip import get_ip_hash


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
    # TODO: show all notice
    return "TO-DO"


@bp.route("/detail/<int:idx>")
def detail(idx: int):
    # TODO: show notice
    return "TO-DO"
