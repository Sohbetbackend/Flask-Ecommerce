from flask import Blueprint

bp = Blueprint("AD", __name__)

from shop.admin import routes, models