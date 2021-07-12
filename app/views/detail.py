from uuid import uuid4

from flask import Blueprint
from flask import render_template

from app.models import Board
from app.alert import with_template

bp = Blueprint(
    name="detail",
    import_name="detail",
    url_prefix="/detail"
)


@bp.route("/<int:idx>")
def show(idx: int):
    board = Board.query.filter_by(
        idx=idx
    ).first()
    if board is None:
        return with_template(
            message="board not Found",
            url="/"
        ), 404

    return render_template(
        "detail/show.html",
        board=board,
        need_axios=True,
        uuid=uuid4().__str__()
    )
