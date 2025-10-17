from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, schemas, crud

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/sso-login")
def sso_login(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Giả lập xác thực SSO, thực tế sẽ xác thực với Microsoft hoặc OAuth provider
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user:
        db_user = crud.create_user(db, user)
    return {"message": "Login successful", "user": db_user.username}
