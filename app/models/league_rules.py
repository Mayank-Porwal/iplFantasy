from datetime import datetime
from db import db
from app.models.leagues import League
from app.models.rules import Rules


class LeagueRules(db.Model):
    __tablename__ = 'league_rules'

    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey(League.id), nullable=False)
    rule_id = db.Column(db.Integer, db.ForeignKey(Rules.id), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"LeagueRules('{self.league_id}', '{self.rule_id}, '{self.value}')"

    def save(self):
        db.session.add(self)
        db.session.commit()
