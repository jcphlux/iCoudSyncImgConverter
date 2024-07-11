from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


def get_engine(db_file):
    return create_engine(f"sqlite:///{db_file}")


def initialize_db(engine):
    Base.metadata.create_all(engine)


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
