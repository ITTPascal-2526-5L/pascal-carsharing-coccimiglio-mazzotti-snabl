from . import db
class Vehicle(db.Model):
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), primary_key=True, nullable=False)
    licence_plate = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    model = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(80), nullable=False)
    fuel = db.Column(db.String(80), nullable=False)
    seats_number = db.Column(db.Integer, nullable=False)
    handicap_seats = db.Column(db.Integer, nullable=False)
    cv = db.Column(db.Integer, nullable=False)
    kw = db.Column(db.Integer, nullable=False)
