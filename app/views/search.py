
from flask import Blueprint


bp = Blueprint(
    name="search",
    import_name="search",
    url_prefix="/search"
)


# To-Do
# 1) search with title
# 1-1) get query from args
# 2) show result with template
