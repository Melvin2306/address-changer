from app.extensions.database import db, CRUDMixin

class User(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(30))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    street_name = db.Column(db.String(40))
    zip_code = db.Column(db.Numeric(8, 0))
    town = db.Column(db.String(20))
    country = db.Column(db.String(20))
    companies = db.relationship('Company', backref='user', lazy=True)

class Company(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(30))
    category = db.Column(db.String(20))
    email_address = db.Column(db.String(40))
    phone_number = db.Column(db.Numeric(15, 0))
    description = db.Column(db.String(100))