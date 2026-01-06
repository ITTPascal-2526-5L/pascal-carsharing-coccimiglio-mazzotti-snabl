from . import db
class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    representative = db.Column(db.String(80), nullable=False)
    mechanical_code = db.Column(db.String(80), unique=True, nullable=False)