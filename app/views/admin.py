from uuid import uuid4
from secrets import token_bytes
from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask_babel import gettext

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


def verify_access_token(access_token: str) -> [str, bool]:
    token = Token.query.filter_by(
        token=access_token,
        is_onetime=False
    ).first()
    if token is not None:
        if token.expire >= datetime.now():
            from_redis = redis.get(f"access:{access_token}")
            if from_redis is not None and get_ip_hash() == from_redis.decode():
                return [token.token, True]

        db.session.delete(token)
        db.session.commit()

    return [None, False]


@bp.get("/verify")
def verify():
    uuid = uuid4().__str__()
    return render_template(
        "admin/verify.html",
        uuid=uuid
    )


@bp.post("/verify")
def verify_post():
    uuid = request.form.get("uuid", None)
    if uuid is None:
        return redirect(url_for("admin.verify", why="captcha"))

    captcha = request.form.get("captcha", None)
    captcha_from_redis = redis.get(f"{get_ip_hash()}:{uuid}")
    if captcha_from_redis is None:
        return redirect(url_for("admin.verify", why="captcha"))

    redis.delete(f"{get_ip_hash()}:{uuid}")
    if captcha == captcha_from_redis.decode():
        one_time_token = request.form.get("token", "")
        token = Token.query.filter_by(
            token=one_time_token,
            is_onetime=True
        ).first()
        if token is not None and token.expire >= datetime.now():
            db.session.delete(token)
            del token

            token = Token()
            token.is_onetime = False
            token.token = token_bytes(60).hex()
            token.expire = datetime.now() + timedelta(hours=1)

            redis.set(f"access:{token.token}", get_ip_hash(), ex=3660)

            db.session.add(token)
            db.session.commit()

            return redirect(url_for("admin.write", token=token.token))

    return redirect(url_for("admin.verify"))


@bp.get("/write")
def write():
    token, result = verify_access_token(request.args.get("token", ""))
    if not result:
        return redirect(url_for(".verify"))

    return render_template(
        "write/write.html",
        no_captcha=True
    )


@bp.post("/write")
def write_post():
    token, result = verify_access_token(request.args.get("token", ""))
    if not result:
        return redirect(url_for(".verify"))

    board = Board()
    board.title = request.form.get("title", None)
    board.content = request.form.get("content", None)
    board.good, board.bad = 0, 0
    board.is_notice = True

    if board.title is not None and board.content is not None:
        board.title = board.title.strip()[:32]
        board.content = board.content.strip()[:60000]
        db.session.add(board)
        db.session.commit()

    return redirect(url_for("admin.write", token=token))


@bp.get("")
def show_all():
    board = Board.query.filter_by(
        is_notice=True
    ).order_by(
        Board.idx.desc()
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

        write_url=url_for("admin.write")
    )
