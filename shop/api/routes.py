from flask import request, jsonify
from shop import db, app
from shop.customers.model import Register


@app.route('/api/register', methods=['GET', 'POST'])
def api_register():
    d={}
    if request.method == "POST":
        name = request.json.get('name')
        contact = request.json.get('contact')

        register = Register.query.filter_by(name=name, contact=contact).first()

        if register is None:
            register = Register(name=name, contact=contact)

            db.session.add(register)
            db.session.commit()

            return jsonify(["Register success"])
        else:
            # Customer already exist
            return jsonify(["Customer already exists!"])


@app.route('/api/login', methods=['GET', 'POST'])
def api_login():
    d = {}
    if request.method == "POST":
        phone = request.form['phone']
        # password = request.form['password']

        login = Register.query.filter_by(phone=phone).first()

        if login is None:

            return jsonify(["Wrong Credentials"])
        else:

            return jsonify(["Success"]) 
