
from flask import Blueprint
from flask import request
from flask import jsonify

from app.ip import get_ip_hash

bp = Blueprint(
    name="recommend",
    import_name="recommend",
    url_prefix="/recommend"
)


@bp.route("/detail", methods=['GET', 'POST'])
def board():
    if request.method == "GET":
        return jsonify({
            "idx": "int",
            "good": "int",
            "bad": "int",
        })
    elif request.method == "POST":
        # To-Do
        # 1) get ip hash
        # 2) append to database

        ip = get_ip_hash()
