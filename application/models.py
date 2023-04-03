from application import db
from datetime import datetime

class Data(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    run_name = db.Column(db.String(10), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    battery_type = db.Column(db.String(15), nullable=False, default='Pouch')
    units_produced = db.Column(db.Integer, nullable=False)
    avg_performance = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return self.product_id