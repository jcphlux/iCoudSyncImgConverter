import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Config


class ConfigLoader:
    def __init__(self, db_path="sqlite:///icloud_sync.db"):
        engine = create_engine(db_path)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_config(self, key):
        config = self.session.query(Config).filter_by(key=key).first()
        if config:
            return os.path.expandvars(config.value)
        else:
            raise ValueError(f"Config key '{key}' not found.")

    def set_config(self, key, value):
        config = self.session.query(Config).filter_by(key=key).first()
        if config:
            config.value = value
        else:
            config = Config(key=key, value=value)
            self.session.add(config)
        self.session.commit()
