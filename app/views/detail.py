from uuid import uuid4
from urllib.parse import urlparse

from flask import Blueprint
from flask import request
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

    parse = urlparse(url=request.referrer)
    if parse.path.startswith("/table"):
        from_table = True
    else:
        from_table = False

    return render_template(
        "detail/show.html",
        board=board,
        need_axios=True,
        uuid=uuid4().__str__(),
        from_table=from_table
    )
