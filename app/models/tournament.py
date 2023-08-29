from datetime import datetime
from db import db


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    season = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    teams = db.Column(db.ARRAY(db.Integer))
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Tournament('{self.name}', '{self.season}', '{self.type}')"

    def save(self):
        db.session.add(self)
        db.session.commit()
