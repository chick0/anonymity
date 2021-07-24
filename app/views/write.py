from uuid import uuid4

from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for

from app import db
from app import redis
from app.ip import get_ip_hash
from app.models import Board

bp = Blueprint(
    name="write",
    import_name="write",
    url_prefix="/write"
)


@bp.get("")
def write():
    uuid = uuid4().__str__()
    return render_template(
        "write/write.html",
        uuid=uuid
    )


@bp.post("")
def post():
    uuid = request.form.get("uuid", None)
    if uuid is None:
        return redirect(url_for(".write", why="captcha"))

    captcha = request.form.get("captcha", None)
    captcha_from_redis = redis.get(f"{get_ip_hash()}:{uuid}")

    if captcha_from_redis is None:
        return redirect(url_for(".write", why="captcha"))

    captcha_from_redis = captcha_from_redis.decode()
    redis.delete(f"{get_ip_hash()}:{uuid}")

    if captcha == captcha_from_redis:
        board = Board()
        board.title = request.form.get("title", None)
        board.content = request.form.get("content", None)

        if board.title is not None and board.content is not None:
            board.title = board.title.strip()[:32]
            board.content = board.content.strip()[:60000]

            if len(board.content) != 0:
                board.good, board.bad = 0, 0

                table_key = request.args.get("table_key", "")
                if len(table_key) == 36:
                    from_redis = redis.get(f"{get_ip_hash()}:{table_key}")
                    if from_redis is not None:
                        board.table_name = from_redis.decode()

                db.session.add(board)
                db.session.commit()

                if len(table_key) == 36:
                    redis.delete(f"{get_ip_hash()}:{table_key}")

                return redirect(url_for("detail.show", idx=board.idx))
    else:
        table_key = request.args.get("table_key", "")
        return redirect(url_for(".write", why="wrong-captcha", table_key=table_key))
