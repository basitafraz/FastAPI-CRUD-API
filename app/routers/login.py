from fastapi import status, HTTPException, Depends, APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, utils, database


router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/")
def login(usercredentials: schemas.Login, db: Session = Depends(database.get_db)):

    user = (
        db.query(models.User).filter(models.User.email == usercredentials.email).first()
    )
    print(usercredentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    if not utils.verify(usercredentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    return {"token": "Example Token"}



