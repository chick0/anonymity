# salt
#   idx int
#   salt string 20
#   created datetime

# board
#   idx int
#   title string 32
#   content text maybe 65535
#   date datetime
#

# reply
#   idx int
#   board_idx int
#   content string 500
#   date datetime

# recommend
#   idx int
#   target_idx int
#   is_board tinyint [T: board, F: reply]
#   vote tinyint [T: Good, F: Bad]
#   date datetime


from . import db

from sqlalchemy import func


class Salt(db.Model):
    idx = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    string = db.Column(
        db.String(20),
        nullable=False
    )

    created = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )


class Board(db.Model):
    idx = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    title = db.Column(
        db.String(32),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )


class Reply(db.Model):
    idx = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    board_idx = db.Column(
        db.Integer,
        nullable=False
    )

    content = db.Column(
        db.String(500),
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )


class Recommend(db.Model):
    idx = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    target_idx = db.Column(
        db.Integer,
        nullable=False
    )

    is_board = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    vote = db.Column(
        db.Boolean,
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )
