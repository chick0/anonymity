from uuid import uuid4
from secrets import token_bytes
from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

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


def verify_access_token(access_token: str) -> bool:
    token = Token.query.filter_by(
        token=access_token
    ).first()
    if token is not None:
        if token.expire >= datetime.now():
            if get_ip_hash() == redis.get(f"access:{access_token}").decode():
                return True
        else:
            db.session.delete(token)
            db.session.commit()

    return False


@bp.route("/verify", methods=['GET', 'POST'])
def verify():
    if request.method == "POST":
        uuid = request.form.get("uuid", None)
        if uuid is not None:
            captcha = request.form.get("captcha", None)
            captcha_from_redis = redis.get(f"{get_ip_hash()}:{uuid}").decode()
            redis.delete(f"{get_ip_hash()}:{uuid}")

            if captcha == captcha_from_redis:
                one_time_token = request.form.get("token", "")
                token = Token.query.filter_by(
                    token=one_time_token
                ).first()
                if token.expire >= datetime.now():
                    db.session.delete(token)
                    del token

                    token = Token()
                    token.is_onetime = False
                    token.token = token_bytes(60).hex()
                    token.expire = datetime.now() + timedelta(hours=1)

                    redis.set(f"access:{token.token}", get_ip_hash(), ex=86400)

                    db.session.add(token)
                    db.session.commit()
                    return redirect(url_for(".write", token=token.token))

    uuid = uuid4().__str__()
    return render_template(
        "admin/verify.html",
        uuid=uuid
    )


@bp.route("/write", methods=['GET', 'POST'])
def write():
    if not verify_access_token(request.args.get("token", "")):
        return redirect(url_for(".verify"))

    if request.method == "POST":
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

    return render_template(
        "write/write.html",
        no_captcha=True
    )


@bp.route("")
def show_all():
    board = Board.query.filter_by(
        is_notice=True
    ).order_by(
        Board.idx.desc()
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
