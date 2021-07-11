
from flask import Flask
from flask_redis import FlaskRedis
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

redis = FlaskRedis()
db = SQLAlchemy()
migrate = Migrate()

APP_NAME = "Anonymity"


def create_app():
    app = Flask(__name__)
    app.config['REDIS_URL'] = "redis://:@192.168.219.100:6379/0"

    from . import config
    app.config.from_object(config)

    from . import views
    for view in views.__all__:
        app.register_blueprint(getattr(views, view).__getattribute__("bp"))

    from . import template_filter
    for name in template_filter.filter_list:
        app.add_template_filter(f=getattr(template_filter, name), name=name)

    from . import models
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

    # init flask redis client!
    redis.init_app(app)

    return app
