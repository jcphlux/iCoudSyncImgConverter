from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, Integer

Base = declarative_base()


class ProcessedFile(Base):
    __tablename__ = "processed_files"
    filename = Column(String, primary_key=True)
    hash = Column(String)
    is_symbolic = Column(Boolean)


class FolderConfig(Base):
    __tablename__ = "folder_config"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_folder = Column(String, unique=True)
    destination_folder = Column(String, unique=True)


class UniversalConfig(Base):
    __tablename__ = "universal_config"
    id = Column(Integer, primary_key=True, autoincrement=True)
    icon_path = Column(String)
    default_behavior = Column(String)
