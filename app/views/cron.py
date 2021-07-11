
from flask import Blueprint


bp = Blueprint(
    name="cron",
    import_name="cron",
    url_prefix="/cron"
)


# TO-DO
# 1) check ip salt lifetime
# 2) vote calc
