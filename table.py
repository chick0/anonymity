from argparse import ArgumentParser

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.config import SQLALCHEMY_DATABASE_URI
from app.models import Table


def get_index() -> int:
    try:
        return int(input("Select index number for edit : ")) - 1
    except ValueError:
        return get_index()


def show_tables():
    session = sessionmaker(bind=engine)()
    tables = session.query(Table).all()

    print("-----< Tables >-----")
    for i, table in enumerate(tables):
        print(f"[{i + 1}] {table.name}: {table.explain}")
    print("--------------------")

    return tables


def add_table(table_name: str, explain: str = None):
    session = sessionmaker(bind=engine)()

    table = Table()
    table.name = table_name
    table.explain = explain

    session.add(table)
    session.commit()

    show_tables()
    print(f"Table Added: {table_name}")


def edit_table():
    session = sessionmaker(bind=engine)()
    tables = show_tables()
    tables_name_ = [table.name for table in tables]

    index = get_index()
    try:
        table = tables[index]
    except IndexError:
        print("Fail to select Table. Cancelled.")
        return

    print("-> <Enter> to skip!")
    tmp_name = input(f"New Name for '{table.name}' : ").strip()[:32]
    if len(tmp_name) != 0 and tmp_name in tables_name_:
        print("Already using name! Cancelled.")
        return

    tmp_explain = input(f"Explain for '{table.name}' : ").strip()[:2000]

    table = session.query(Table).filter_by(
        name=table.name
    ).first()
    table.name = tmp_name
    table.explain = table.explain if len(tmp_explain) == 0 else tmp_explain
    session.commit()
    show_tables()


def del_table():
    session = sessionmaker(bind=engine)()
    tables = show_tables()

    index = get_index()
    try:
        table = tables[index]
    except IndexError:
        print("Fail to select Table. Cancelled.")
        return

    session.query(Table).filter_by(
        name=table.name
    ).delete()
    session.commit()
    show_tables()


if __name__ == "__main__":
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    parser = ArgumentParser(description="Table manager")
    parser.add_argument("--show",
                        help="show all tables",
                        action="store_const", const=True)
    parser.add_argument("--add",
                        help="add new table",
                        action="store_const", const=True)
    parser.add_argument("--edit",
                        help="edit table data",
                        action="store_const", const=True)
    parser.add_argument("--delete",
                        help="delete table",
                        action="store_const", const=True)

    args = parser.parse_args()
    if args.show:
        show_tables()
    elif args.add:
        tables_name = [table.name for table in show_tables()]
        tmp = input("New table name: ").strip()[:32]
        if tmp in tables_name:
            print("Already created table! Cancelled.")
        else:
            if len(tmp) >= 1:
                add_table(
                    table_name=tmp,
                    explain=input("Explain the table: ").strip()[:2000]
                )
            else:
                print("Table name is too short. Cancelled.")
    elif args.edit:
        edit_table()
    elif args.delete:
        del_table()
    else:
        parser.print_help()