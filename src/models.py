from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, Integer

Base = declarative_base()


class ProcessedFile(Base):
    __tablename__ = "processed_files"
    filename = Column(String, primary_key=True)
    hash = Column(String)
    is_symbolic = Column(Boolean)


class Config(Base):
    __tablename__ = "config"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, unique=True)
    value = Column(String)
