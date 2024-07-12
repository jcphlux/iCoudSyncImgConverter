from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from models import Base, FolderConfig, UniversalConfig

DATABASE_URL = "sqlite:///icloud_sync.db"

# Create an engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)


def get_session():
    """Get a new session for database operations."""
    return Session()


def initialize_db():
    """Initialize the database and create tables."""
    Base.metadata.create_all(engine)
    session = get_session()

    # Check if config table is empty and add default values
    if not session.query(UniversalConfig).count():
        default_config = UniversalConfig(
            icon_path="imgs/iCloudSync_icon.png", default_behavior="symbolic"
        )
        session.add(default_config)
        session.commit()

    if not session.query(FolderConfig).count():
        default_folder_config = FolderConfig(
            source_folder="%USERPROFILE%\\Pictures\\iCloud Photos\\Photos",
            destination_folder="%USERPROFILE%\\Pictures\\iCloudSync",
        )

        session.add(default_folder_config)
        session.commit()


def is_db_initialized():
    """Check if the database and tables are initialized."""
    inspector = inspect(engine)
    return inspector.has_table("config") and inspector.has_table("processed_files")
