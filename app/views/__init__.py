from os import path
from os import listdir

__all__ = [
    view_name[:-3]
    for view_name in listdir(path.dirname(__file__)) if not view_name.startswith("__")
]


from app.views import *
