
from flask import Flask


APP_NAME = "Anonymity"


def create_app():
    app = Flask("Anonymity")

    from . import views
    for view in views.__all__:
        app.register_blueprint(getattr(views, view).__getattribute__("bp"))

    return app
