from flask import jsonify, request
from shop.products.models import Category
from shop.api import bp


@bp.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    return jsonify(Category.query.get_or_404(id).to_dict())


@bp.route('/categories', methods=['GET'])
def get_categories():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Category.to_collection_dict(Category.query, page, per_page, 'api.get_categories')
    return jsonify(data)

