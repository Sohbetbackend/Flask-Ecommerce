from shop import db
from datetime import datetime


class ProductAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=page, per_page=per_page,
                                   error_out=False)
        data = {
            'data': [item.to_dict() for item in resources.items],
        }
        return data


class Addproduct(db.Model, ProductAPIMixin):
    __searchable__ = ['name','desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image1.jpg')


    def __repr__(self):
        return '<Post %r>' % self.name

    
    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category_id,   
            'stock': self.stock,
            'desc': self.desc,
            'image_prod_url': self.image_1,
        }
        return data


class CategoryAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=page, per_page=per_page,
                                   error_out=False)
        data = {
            'data': [item.to_dict() for item in resources.items],
        }
        return data


class Category(db.Model, CategoryAPIMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    image_category = db.Column(db.String(150))


    def __repr__(self):
        return '<Category %r>' % self.name


    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'image_cat_url': self.image_category,
        }
        return data


class BannerAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=page, per_page=per_page,
                                   error_out=False)
        data = {
            'data': [item.to_dict() for item in resources.items],
        }
        return data


class Banner(db.Model, BannerAPIMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    image_banner = db.Column(db.String(250))

    def __repr__(self):
        return '<Banner %r>' % self.name


    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'image_ban_url': self.image_banner,
        }
        return data


db.create_all()
