from shop import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json
from flask import url_for


@login_manager.user_loader
def user_loader(user_id):
    return Customer.query.get(user_id)


class CustomerAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=page, per_page=per_page,
                                   error_out=False)
        data = {
            'data': [item.to_dict() for item in resources.items],
        }
        return data


class Customer(db.Model, UserMixin, CustomerAPIMixin):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), unique= False)
    password = db.Column(db.String(200), unique= False)
    contact = db.Column(db.String(50), unique= False)
    address = db.Column(db.String(50), unique= False)
    orders = db.relationship('CustomerOrder', backref='customer', lazy='dynamic')


    def __repr__(self):
        return '<Register %r>' % self.name

    
    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'contact': self.contact,
            'order_count': self.orders.count(),
            'address': self.address,
        }
        return data
    
        
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
            

class OrdersAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=page, per_page=per_page,
                                   error_out=False)
        data = {
            'data': [item.to_dict() for item in resources.items],
        }
        return data


class CustomerOrder(db.Model, OrdersAPIMixin):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, unique=False)
    orders = db.Column(JsonEcodedDict)
    date_ordered = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer_name = db.Column(db.String(250))
    customer_contact = db.Column(db.String(250))


    def __repr__(self):
        return'<CustomerOrder %r>' % self.id

    def to_dict(self):
        data = {
            'id': self.id,
            'orders': self.orders,
            # 'date_ordered' : self.date_ordered,
            'customer_name': self.customer_name,
            'customer_contact': self.customer_contact,
        }
        return data
        

db.create_all()