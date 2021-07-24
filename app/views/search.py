
from flask import Blueprint
from flask import request
from flask import render_template

from app.models import Board

bp = Blueprint(
    name="search",
    import_name="search",
    url_prefix="/search"
)


@bp.get("")
def form():
    query = request.args.get("title", "", type=str)
    if len(query) != 0:
        results = Board.query.filter(
            Board.title.ilike(f"%{query}%")
        ).limit(10).all()
    else:
        results = []

    return render_template(
        "search/form.html",
        query=query,
        results=results
    )
