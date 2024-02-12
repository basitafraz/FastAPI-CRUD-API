from fastapi import status, HTTPException, Depends, APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, utils, database, oAuth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/", response_model= schemas.Token)
def login(usercredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = (
        db.query(models.User).filter(models.User.email == usercredentials.username).first()
    )
    print(usercredentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    if not utils.verify(usercredentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
        
    access_token = oAuth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}



