from datetime import datetime
from db import db


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False)
    season_id = db.Column(db.Integer, nullable=False)
    home_team_id = db.Column(db.Integer, nullable=False)
    away_team_id = db.Column(db.Integer, nullable=False)
    venue_id = db.Column(db.Integer, nullable=False)
    schedule = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, default=0)
    # lineup = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Match('{self.home_team_id}' vs '{self.away_team_id}' on '{self.schedule}' at '{self.venue_id}')"

    def save(self):
        db.session.add(self)
        db.session.commit()
