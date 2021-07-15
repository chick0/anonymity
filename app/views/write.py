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


@bp.route("", methods=['GET', 'POST'])
def write():
    if request.method == "POST":
        uuid = request.form.get("uuid", None)
        if uuid is None:
            return redirect(url_for(".write"))

        captcha = request.form.get("captcha", None)
        captcha_from_redis = redis.get(f"{get_ip_hash()}:{uuid}").decode()
        redis.delete(f"{get_ip_hash()}:{uuid}")

        if captcha == captcha_from_redis:
            board = Board()
            board.title = request.form.get("title", None)
            board.content = request.form.get("content", None)

            if board.title is not None and board.content is not None:
                board.title = board.title[:32]
                board.content = board.content.strip()[:60000]

                if len(board.content) != 0:
                    board.good, board.bad = 0, 0

                    db.session.add(board)
                    db.session.commit()

                    return redirect(url_for("detail.show", idx=board.idx))

    uuid = uuid4().__str__()

    return render_template(
        "write/write.html",
        uuid=uuid
    )
