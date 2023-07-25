from datetime import datetime
from db import db
from util import LeagueType


class UserLeague(db.Model):
    __tablename__ = 'user_league'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    league_type = db.Column(db.Enum(LeagueType))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    join_code = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"UserLeague('League {self.name}' created by '{self.owner}' with code: '{self.join_code}')"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()


class LeagueInfo(db.Model):
    __tablename__ = 'league_info'

    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey('user_league.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('user_team.id'), nullable=False)
    team_rank = db.Column(db.Integer, default=-1)

    def __repr__(self):
        return f"LeagueInfo('User: {self.user_id} joined the league: {self.league_id} with team: {self.team_id}')"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
