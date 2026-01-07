from datetime import datetime
from . import db
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    surname = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phonenumber = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    licenseid = db.Column(db.String(120), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    priceperkm = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)