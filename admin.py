from secrets import token_bytes
from argparse import ArgumentParser
from datetime import datetime
from datetime import timedelta

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.config import SQLALCHEMY_DATABASE_URI
from app.models import Token


def create_one_time_token():
    session = sessionmaker(bind=engine)()
    token = Token()
    token.is_onetime = True
    token.token = token_bytes(60).hex()
    token.expire = datetime.now() + timedelta(minutes=1)

    session.add(token)
    session.commit()
    return token.token


def show_logins():
    session = sessionmaker(bind=engine)()
    sessions = session.query(Token).all()

    print("-----< Sessions >-----")
    for i, x in enumerate(sessions):
        print(f"[{i + 1}] {x.token[:8]} : {'one-time' if x.is_onetime else 'access'}")
    print("----------------------")

    return sessions


def delete_all_session():
    session = sessionmaker(bind=engine)()
    for token in session.query(Token).all():
        session.query(Token).filter_by(
            idx=token.idx
        ).delete()

    session.commit()
    show_logins()


if __name__ == "__main__":
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    parser = ArgumentParser(description="'Anonymity' Admin token manager")
    parser.add_argument("--show",
                        help="show all admin sessions",
                        action="store_const", const=True)
    parser.add_argument("--create",
                        help="create new one-time token",
                        action="store_const", const=True)
    parser.add_argument("--logout",
                        help="delete all login sessions",
                        action="store_const", const=True)

    args = parser.parse_args()
    if args.show:
        show_logins()
    if args.create:
        one_time_token = create_one_time_token()
        print(f"One-time token is '{one_time_token}'")
    if args.logout:
        delete_all_session()
