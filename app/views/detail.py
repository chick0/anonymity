# get all of reply
# but use page

from flask import Blueprint


bp = Blueprint(
    name="detail",
    import_name="detail",
    url_prefix="/detail"
)
