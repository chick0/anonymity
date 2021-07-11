from os import environ

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = environ.get("anonymity_sql", default="sqlite:///anonymity.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# REDIS
REDIS_URL = environ.get("anonymity_redis", default="redis://:@localhost:6379/0")
