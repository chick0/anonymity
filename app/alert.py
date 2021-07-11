
from flask import render_template_string


def with_template(message: str, url: str = None):
    source = " ".join([
        "<script>",
        "window.alert('{{ message }}');",
        "location.replace('{{ url|safe }}');",
        "</script>"
    ])

    return render_template_string(
        source=source,
        message=message,
        url=url if url is not None else "/"
    )
