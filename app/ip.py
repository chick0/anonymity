from secrets import token_bytes
from hashlib import sha384
from datetime import datetime
from datetime import timedelta

from flask import request

from app import db
from app.models import Salt


def gen_salt() -> Salt:
    salt = Salt()
    salt.string = token_bytes(20).hex()

    db.session.add(salt)
    db.session.commit()
    return salt


def get_salt() -> str:
    salt = Salt.query.first()
    if salt is None:
        salt = gen_salt()

    if salt.created > datetime.now() + timedelta(days=1):
        salt = gen_salt()

    return salt.string


def get_ip_hash() -> str:
    def get_ip() -> str:
        header_list = [
            "X-Forwarded-For",
            "CF-Connecting-IP"
        ]
        for header in header_list:
            tmp = request.headers.get(header, "")
            if len(tmp) >= 7:
                return tmp

        return request.remote_addr

    ip = get_ip()
    salt = get_salt()

    return sha384(f"{ip}+{salt}".encode()).hexdigest()
