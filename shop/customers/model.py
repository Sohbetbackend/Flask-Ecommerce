from shop import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json

@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)

class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), unique= False)
    email = db.Column(db.String(50), unique= True)
    password = db.Column(db.String(200), unique= False)
    city = db.Column(db.String(50), unique= False)
    contact = db.Column(db.String(50), unique= False)
    address = db.Column(db.String(50), unique= False)
    orders = db.relationship('CustomerOrder', backref='customer', lazy='dynamic')

    def __repr__(self):
        return '<Register %r>' % self.name


class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    orders = db.Column(JsonEcodedDict)
    date_ordered = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    register_id = db.Column(db.Integer, db.ForeignKey('register.id'))


    def __repr__(self):
        return'<CustomerOrder %r>' % self.id



db.create_all()
