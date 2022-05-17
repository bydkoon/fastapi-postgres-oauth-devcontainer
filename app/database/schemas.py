from pydantic import BaseModel


class UserBase(BaseModel):
    """database User type"""
    uid: str
    email: str
    nickname: str
    gender: str
    age: int


class User(UserBase):
    """class orm type"""
    id: int

    class Config:
        orm_mode = True