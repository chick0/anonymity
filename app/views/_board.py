
from flask import Blueprint
from flask import jsonify
from sqlalchemy.sql.expression import func

from app.models import Board


bp = Blueprint(
    name="board",
    import_name="board",
    url_prefix="/board"
)


@bp.get("/random")
def random():
    board = Board.query.order_by(func.random()).first()
    if board is None:
        return jsonify({
            "error": "board is empty"
        }), 404

    table_name = "" if board.table_name is None else board.table_name
    if board.is_notice:
        table_name = "admin"

    return jsonify({
        "idx": board.idx,
        "head": {
            "date": board.date,
            "table_name": table_name
        },
        "body": {
            "title": board.title,
            "content": board.content,
            "vote": {
                "good": board.good,
                "bad": board.bad,
            }
        }
    })
