
from flask import Blueprint


bp = Blueprint(
    name="cron",
    import_name="cron",
    url_prefix="/cron"
)
