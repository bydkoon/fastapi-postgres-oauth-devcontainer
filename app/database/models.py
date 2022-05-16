from sqlalchemy import Column, Integer, String, CHAR
from database.database import Base


class Users(Base):
    __tablename__ = "users"

    uid = Column(String(255), primary_key=True, unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    nickname = Column(String(40))
    gender = Column(CHAR(2))
    age = Column(Integer(4))