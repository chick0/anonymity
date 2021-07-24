def check_table_name(obj):
    return obj.table_name is not None and len(obj.table_name) > 0


def write_url(url):
    if len(url) == 0:
        from flask import url_for
        return url_for("write.write")

    return url


# do not touch this
filter_list = [name for name in dir() if not name.startswith("_")]
# do not touch this
