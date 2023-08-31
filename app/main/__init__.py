# flask
from flask import Blueprint


bp = Blueprint("main", __name__)


# local
from app.main import routes
