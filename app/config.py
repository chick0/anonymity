from os import environ

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY", default="sqlite:///:memory:")
SQLALCHEMY_TRACK_MODIFICATIONS = False
