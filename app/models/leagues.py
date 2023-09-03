from datetime import datetime
from db import db
from app.utils.leagues import LeagueType
from app.models.tournament import Tournament


class League(db.Model):
    __tablename__ = 'league'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey(Tournament.id))
    name = db.Column(db.String(50), nullable=False)
    league_type = db.Column(db.Enum(LeagueType))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    join_code = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"League('League {self.name}' created by '{self.owner}' with code: '{self.join_code}')"

    def save(self):
        db.session.add(self)
        db.session.commit()
