# salt
#   idx int
#   salt string 20
#   created datetime

# TODO: admin
#   idx int
#   title string 32
#   content text
#   date datetime
#   good int
#   bad int

# TODO: token
#   idx int
#   is_onetime tinyint [T: one-time, F: access]
#   token text
#   expire datetime NOT-NULL NO-DEFAULT

# table
#   name string 32 [UNIQUE PRIMARY_KEY]
#   explain text

# board
#   idx int
#   title string 32
#   content text maybe 65535
#   date datetime
#   good int
#   bad int
#   table_name string 32 [nullable]

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
#   used tinyint [T: used, F: not used]
#   ip string 96


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


class Table(db.Model):
    name = db.Column(
        db.String(32),
        unique=True,
        primary_key=True,
        nullable=False
    )
    explain = db.Column(
        db.Text
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

    good = db.Column(
        db.Integer
    )
    bad = db.Column(
        db.Integer
    )
    table_name = db.Column(
        db.String(32)
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

    used = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    ip = db.Column(
        db.String(96)
    )
