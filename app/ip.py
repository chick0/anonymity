from secrets import token_bytes
from hashlib import sha384


def get_salt() -> str:
    def gen_salt() -> str:
        return token_bytes(20).hex()

    # try to get salt from database

    # on fail
    salt = gen_salt()

    return salt


def get_ip_hash() -> str:
    def get_ip() -> str:
        return ""

    ip = get_ip()
    salt = get_salt()

    return sha384(f"{ip}+{salt}".encode()).hexdigest()
