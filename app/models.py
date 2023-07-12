from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from app.leagues.utils import LeagueType


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(30))
    image_file = db.Column(db.String(50), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def save(self):
        db.session.add(self)
        db.session.commit()


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


class UserTeam(db.Model):
    __tablename__ = 'user_team'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    players = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"UserTeam('{self.name}', '{self.players}')"

    def save(self):
        db.session.add(self)
        db.session.commit()


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    ipl_team = db.Column(db.String(30), nullable=False)
    cap = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Player('{self.name}', '{self.id}', '{self.cap}')"


class RevokedAccessTokens(db.Model):
    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
