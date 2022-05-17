
from sqlalchemy import Column, String, CHAR
from sqlalchemy.dialects.mysql import SMALLINT
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Users(Base):
    """Database Users"""
    __tablename__ = "users"

    uid = Column(String(255), primary_key=True, unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    nickname = Column(String(40))
    gender = Column(CHAR(2))
    age = Column(SMALLINT(4))