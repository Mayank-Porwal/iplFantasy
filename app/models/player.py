from datetime import datetime
from db import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.Integer, nullable=False)
    ipl_team = db.Column(db.Integer, nullable=False)
    cap = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.String(256), nullable=False, default='default.jpeg')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()
