from flask import jsonify, request, url_for
from shop import db
from shop.api import bp
from shop.customers.model import CustomerOrder
from shop.api.errors import bad_request


@bp.route('/orders', methods=['POST', 'GET'])
def orders():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 100, type=int), 100)
    data = CustomerOrder.to_collection_dict(CustomerOrder.query, page, per_page, 'api.get_orders')
    return jsonify(data)


@bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json() or {}
    if 'customer_name' not in data or 'customer_contact' not in data or 'orders' not in data:
        return bad_request('must include customer_name, customer_contact and orders fields')
    order = CustomerOrder()
    order.from_dict(data, new_order=True)
    db.session.add(order)
    db.session.commit()
    response = jsonify(order.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_order', id=order.id)
    return response
