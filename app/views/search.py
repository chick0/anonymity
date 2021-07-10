# search with **title** only

from flask import Blueprint


bp = Blueprint(
    name="search",
    import_name="search",
    url_prefix="/search"
)
