from flask import jsonify, request
from shop.products.models import Addproduct
from shop.api import bp


@bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    return jsonify(Addproduct.query.get_or_404(id).to_dict())


@bp.route('/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Addproduct.to_collection_dict(Addproduct.query, page, per_page, 'api.get_products')
    return jsonify(data)


