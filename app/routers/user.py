from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(
    prefix= "/users",
    tags= ["users"]
)


@router.get("/", response_model=list[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    try:
        db_users = db.query(models.User).all()
        if db_users:
            return db_users
        else:
            raise HTTPException(status_code=404, detail="No users found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(
            status_code=400, detail="An error occurred while creating the user."
        )


@router.put("/{user_id}")
def update_user(
    user_id: int, user_data: schemas.UserCreate, db: Session = Depends(get_db)
):
    try:
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        if db_user:
            for field, value in user_data.dict().items():
                setattr(db_user, field, value)
            db.commit()
            return {"message": f"User with ID {user_id} updated successfully"}
        else:
            raise HTTPException(
                status_code=404, detail=f"User with ID {user_id} not found"
            )
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return {"message": f"User with ID {user_id} deleted successfully"}
        else:
            raise HTTPException(
                status_code=404, detail=f"User with ID {user_id} not found"
            )
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            return user
        else:
            raise HTTPException(
                status_code=404, detail=f"User with ID {user_id} not found"
            )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
