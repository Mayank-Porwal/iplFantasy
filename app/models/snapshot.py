from datetime import datetime
from db import db
from app.models.teams import UserTeam
from app.models.leagues import League


class Snapshot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey(League.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey(UserTeam.id), nullable=False)
    team_snapshot = db.Column(db.JSON)
    match_points = db.Column(db.Float, default=0.0)
    cumulative_points = db.Column(db.Float, default=0.0)
    rank = db.Column(db.Integer, default=-1)
    remaining_substitutes = db.Column(db.Integer, default=250)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Snapshot('{self.match_id}' - '{self.league_id}' - '{self.user_id}' - '{self.team_id}')"

    def save(self):
        db.session.add(self)
        db.session.commit()
