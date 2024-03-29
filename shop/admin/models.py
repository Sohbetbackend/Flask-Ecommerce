from shop import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180),unique=False, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.email
