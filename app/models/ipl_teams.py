from datetime import datetime
from db import db


class IplTeams(db.Model):
    __tablename__ = 'ipl_teams'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    image = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"IplTeams('{self.name}')"

    def save(self):
        db.session.add(self)
        db.session.commit()
