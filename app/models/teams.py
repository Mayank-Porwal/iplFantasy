from datetime import datetime
from db import db


class UserTeam(db.Model):
    __tablename__ = 'user_team'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    players = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"UserTeam('{self.name}', '{self.players}')"

    def save(self):
        db.session.add(self)
        db.session.commit()
