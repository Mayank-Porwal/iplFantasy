from db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(30))
    image_file = db.Column(db.String(50), nullable=False, default='default.jpeg')
    password = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.email}', '{self.image_file}')"

    def save(self):
        db.session.add(self)
        db.session.commit()


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
