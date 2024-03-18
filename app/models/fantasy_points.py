from datetime import datetime
from db import db
from app.models.leagues import League


class FantasyPoints(db.Model):
    __tablename__ = 'fantasy_points'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey(League.id), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    points = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"FantasyPoints('{self.match_id}' - '{self.player_id}' - '{self.league_id}')"

    def save(self):
        db.session.add(self)
        db.session.commit()
