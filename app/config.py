from os import environ

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = environ.get("anonymity_sql", default="sqlite:///anonymity.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# REDIS
REDIS_URL = environ.get("anonymity_redis", default="redis://:@localhost:6379/0")

# Babel
LANGUAGES = {
    "en": "English",
    "ko": "Korean",
}

LANGUAGE_MAP = {
    "en": "en",
    "en-US": "en",

    "ko": "ko",
    "ko-KR": "ko",
}
