from database import crud, schemas, models
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_db

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user_info: schemas.UserBase, session: Session = Depends(get_db)):
    db_user = (
        session.query(models.Users)
        .filter(models.Users.nickname == user_info.nickname)
        .first()
    )

    if db_user:
        raise HTTPException(status_code=400, detail="Nickname already registered")
    return crud.create_user(session, user_info)


@router.get(path="/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, session: Session = Depends(get_db)):
    user = session.query(models.Users).filter(models.Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 User가 없습니다.")
    return user


@app.put(path="/users/{user_id}", response_model=schemas.User)
def put_user(
    user_id: int, new_info: schemas.UserBase, session: Session = Depends(get_db)
):
    user_info = crud.update_user_info(session, user_id, new_info)
    return user_info


@app.delete(path="/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_db)):
    user_info = session.query(models.Users).get(user_id)

    if user_info is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 User가 없습니다.")

    session.delete(user_info)
    session.commit()

    return user_info