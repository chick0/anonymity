
from flask import Blueprint
from flask import render_template

from app.models import Board


bp = Blueprint(
    name="search",
    import_name="search",
    url_prefix="/search"
)


@bp.route("/t/<str:query>")
def title(query: str):
    board = Board.query.filter_by(
        title=Board.title.ilike(query)
    ).limit(50).all()

    return render_template(
        "search/result.html",
        board=board
    )


@bp.route("/c/<str:query>")
def content(query: str):
    board = Board.query.filter_by(
        content=Board.title.ilike(query)
    ).limit(50).all()

    return render_template(
        "search/result.html",
        board=board
    )
