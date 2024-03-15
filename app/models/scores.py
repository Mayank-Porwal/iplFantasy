from datetime import datetime
from db import db


class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)

    # Batting related columns
    runs_scored = db.Column(db.Integer, default=0)
    balls_faced = db.Column(db.Integer, default=0)
    sixes = db.Column(db.Integer, default=0)
    fours = db.Column(db.Integer, default=0)
    strike_rate = db.Column(db.Float, default=0.0)
    dismissed = db.Column(db.Boolean, nullable=True, default=False)

    # Bowling related columns
    wickets = db.Column(db.Integer, default=0)
    balls_bowled = db.Column(db.Integer, default=0)
    dots = db.Column(db.Integer, default=0)
    maidens = db.Column(db.Integer, default=0)
    economy = db.Column(db.Float, default=0.0)

    # Fielding related columns
    catches = db.Column(db.Integer, default=0)
    run_outs = db.Column(db.Integer, default=0)

    # Award related columns
    man_of_the_match = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Scores('{self.match_id}' - '{self.player_id}'"

    def save(self):
        db.session.add(self)
        db.session.commit()
