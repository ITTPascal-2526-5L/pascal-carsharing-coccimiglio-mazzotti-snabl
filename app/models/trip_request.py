from . import db

class TripRequest(db.Model):
    trip_code = db.Column(db.Integer, db.ForeignKey('trip.code'), primary_key=True, nullable=False)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passenger.id'), nullable=False)
    pickup_point = db.Column(db.String(120), nullable=False)