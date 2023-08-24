from flask import request, jsonify, abort
from shop.customers.model import Customer
from shop import db
from shop.api import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    d = {}
    if request.method == "POST":
        contact = request.form['contact']

        login = Customer.query.filter_by(contact=contact).first()

        if login is None:

            return jsonify(["Wrong Credentials"])
        else:

            return jsonify(["Success"]) 


@bp.route('/register', methods=['GET', 'POST'])
def register():
    name = request.json.get('name')
    contact = request.json.get('contact')
    password = request.json.get('password')
    address = request.json.get('address')
    if name is None or contact is None or password is None or address is None:
        abort(400)
    if Customer.query.filter_by(contact=contact).first() is not None:
        abort(400)
    register = Customer(name=name, contact=contact, password=password, address=address)
    db.session.add(register)
    db.session.commit()
    return jsonify({'name': register.name, 'contact': register.contact, 'address': register.address}), 201
    