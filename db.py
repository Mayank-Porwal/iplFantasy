import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

db = SQLAlchemy()


def conn():
    url = os.getenv('DATABASE_URL')
    engine = create_engine(url)
    return engine.connect()
