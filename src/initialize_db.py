from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Config


def initialize_db():
    engine = create_engine("sqlite:///icloud_sync.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if config table is empty and add default values
    if not session.query(Config).count():
        default_configs = [
            Config(
                key="folder_to_watch",
                value="%USERPROFILE%\\Pictures\\iCloud Photos\\Photos",
            ),
            Config(
                key="destination_folder",
                value="%USERPROFILE%\\Pictures\\iCloudSync",
            ),
            Config(key="icon_path", value="imgs\\iCloudSync_icon.svg"),
            Config(key="icon_size", value="24"),
            Config(key="default_behavior", value="symbolic"),
        ]
        session.add_all(default_configs)
        session.commit()


if __name__ == "__main__":
    initialize_db()
