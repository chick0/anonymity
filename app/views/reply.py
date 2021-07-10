# reply add api

from flask import Blueprint


bp = Blueprint(
    name="reply",
    import_name="reply",
    url_prefix="/reply"
)
