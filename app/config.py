from os import environ

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = environ.get("anonymity_sql", default="sqlite:///anonymity.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False
