
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import render_template
from flask import redirect
from flask import url_for


from app import db
from app.models import Board
from app.models import Reply


bp = Blueprint(
    name="reply",
    import_name="reply",
    url_prefix="/reply"
)


@bp.route("/", methods=['POST'])
def add():
    board_idx = request.args.get("board_idx", -1, type=int)
    board = Board.query.filter_by(
        idx=board_idx
    ).first()
    if board is None:
        return jsonify({
            "message": "board not found",
            "result": "failed"
        }), 404

    reply = Reply()
    reply.board_idx = board_idx
    reply.content = request.form.get("content").strip()

    if len(reply.content) == 0:
        return jsonify({
            "result": "failed"
        })

    db.session.add(reply)
    db.session.commit()
    return jsonify({
        "idx": reply.idx,
        "result": "ok"
    })


@bp.route("/<int:idx>")
def get(idx: int):
    reply_list = Reply.query.filter_by(
        board_idx=idx
    ).order_by(Reply.idx.desc()).paginate(page=request.args.get("page", 1, type=int))

    result = []
    for reply in reply_list.items:
        result.append({
            "idx": reply.idx,
            "content": reply.content,
            "date": reply.date
        })

    return jsonify({
        "head": {
            "board_idx": idx,
            "page": reply_list.page,
            "total_page": reply_list.pages
        },
        "body": result
    })


@bp.route("/show/<int:idx>")
def show(idx: int):
    reply = Reply.query.filter_by(
        idx=idx
    ).first()
    if reply is None:
        return redirect(url_for("board.show_all"))

    return render_template(
        "reply/show.html",
        reply=reply
    )
