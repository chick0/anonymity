
from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for

from app import db
from app.models import Board

bp = Blueprint(
    name="write",
    import_name="write",
    url_prefix="/write"
)


@bp.route("", methods=['GET', 'POST'])
def write():
    if request.method == "POST":
        board = Board()
        board.title = request.form.get("title", None)
        board.content = request.form.get("content", None)

        if board.title is not None and board.content is not None:
            db.session.add(board)
            db.session.commit()

            return redirect(url_for("detail.show", idx=board.idx))

    return render_template(
        "write/write.html",
    )
