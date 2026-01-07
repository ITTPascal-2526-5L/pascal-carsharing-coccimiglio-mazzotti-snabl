from datetime import datetime
from . import db

class Trip(db.Model):
    code = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)