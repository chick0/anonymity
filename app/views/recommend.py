# good / bad

from flask import Blueprint


bp = Blueprint(
    name="recommend",
    import_name="recommend",
    url_prefix="/recommend"
)
