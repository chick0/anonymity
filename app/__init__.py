from threading import Thread

from flask import Flask
from flask import request
from flask_babel import Babel
from flask_redis import FlaskRedis
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

babel = Babel()
redis = FlaskRedis()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # load config
    from . import config
    app.config.from_object(config)

    # blueprint init
    from . import views
    for view in views.__all__:
        app.register_blueprint(getattr(views, view).__getattribute__("bp"))

    # template filter init
    from . import template_filter
    for name in template_filter.filter_list:
        app.add_template_filter(f=getattr(template_filter, name), name=name)

    # i18n
    babel.init_app(app=app)

    @babel.localeselector
    def get_locale():
        return app.config['LANGUAGE_MAP'][request.accept_languages.best_match(app.config['LANGUAGE_MAP'].keys())]

    # client init
    redis.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

    # background task
    from . import task
    Thread(target=task.core, args=(app,), daemon=True).start()

    return app
