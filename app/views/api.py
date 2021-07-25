
from flask import Blueprint

from . import _board

bp = Blueprint(
    name="api",
    import_name="api",
    url_prefix="/api"
)


bp.register_blueprint(blueprint=_board.bp)
