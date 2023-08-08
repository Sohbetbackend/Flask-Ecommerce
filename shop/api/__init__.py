from flask import Blueprint

bp = Blueprint('api', __name__)

from shop.api import customers, errors, products_api, categories, banners, auth, orders