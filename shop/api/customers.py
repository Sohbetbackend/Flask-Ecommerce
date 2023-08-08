from flask import jsonify, request
from shop.customers.model import Customer
from shop.api import bp


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(Customer.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 100, type=int), 100)
    data = Customer.to_collection_dict(Customer.query, page, per_page, 'api.get_users')
    return jsonify(data)
