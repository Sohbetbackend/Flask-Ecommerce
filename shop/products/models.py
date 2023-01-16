from shop import db
from datetime import datetime


class Addproduct(db.Model):
    __seachbale__ = ['name','desc']
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
    image_prod_url = db.Column(db.Text)


    def __repr__(self):
        return '<Post %r>' % self.name



class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    image_category = db.Column(db.String(150))
    image_cat_url = db.Column(db.Text)


    def __repr__(self):
        return '<Catgory %r>' % self.name


class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    image_banner = db.Column(db.String(250))
    image_ban_url = db.Column(db.Text)

    def __repr__(self):
        return '<Banner %r>' % self.name


db.create_all()
