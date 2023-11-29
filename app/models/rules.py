from datetime import datetime
from db import db


class Rules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    rule = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Rules('{self.id}', '{self.rule}')"

    def save(self):
        db.session.add(self)
        db.session.commit()
