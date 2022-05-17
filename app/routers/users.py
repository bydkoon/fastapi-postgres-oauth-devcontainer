from fastapi import APIRouter, HTTPException, Depends
from ..sql import crud, schemas, models, database
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.User)
def create_user(user_info: schemas.UserBase, session: Session = Depends(database.get_db)):
    """db create user """
    db_user = (
        session.query(models.Users)
        .filter(models.Users.nickname == user_info.nickname)
        .first()
    )

    if db_user:
        raise HTTPException(status_code=400, detail="Nickname already registered")
    return crud.create_user(session, user_info)


@router.get(path="/{user_id}", response_model=schemas.User)
def get_user(user_id: int, session: Session = Depends(database.get_db)) -> schemas.User:
    """ get user_id on db"""
    user = session.query(models.Users).filter(models.Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 User가 없습니다.")
    return user


@router.put(path="/{user_id}", response_model=schemas.User)
def put_user(
    user_id: int, new_info: schemas.UserBase, session: Session = Depends(database.get_db))-> schemas.User: 
    """ update user """
    user_info : schemas.User = crud.update_user_info(session, user_id, new_info)
    return user_info


@router.delete(path="/{user_id}")
def delete_user(user_id: int, session: Session = Depends(database.get_db)):
    """ delete user """
    user_info = session.query(models.Users).get(user_id)

    if user_info is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 User가 없습니다.")
    session.delete(user_info)
    session.commit()

    return user_info