
from flask import Blueprint


bp = Blueprint(
    name="write",
    import_name="write",
    url_prefix="/write"
)
