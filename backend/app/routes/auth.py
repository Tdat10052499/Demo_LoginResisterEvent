from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, models, schemas, crud

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", response_model=schemas.UserRead)
def register(user: schemas.UserRegister, db: Session = Depends(database.get_db)):
    """
    Đăng ký tài khoản mới với username, email và password
    """
    # Kiểm tra username đã tồn tại
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Kiểm tra email đã tồn tại
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Tạo user mới
    db_user = crud.register_user(db, user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed"
        )
    
    return db_user

@router.post("/login", response_model=schemas.UserRead)
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    """
    Đăng nhập với username và password
    """
    db_user = crud.authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    return db_user

@router.post("/sso-login")
def sso_login(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    SSO login (Microsoft, Google, etc.)
    """
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user:
        db_user = crud.create_user(db, user)
    return {"message": "Login successful", "user": db_user}
