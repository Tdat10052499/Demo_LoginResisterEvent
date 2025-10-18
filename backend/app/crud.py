from sqlalchemy.orm import Session
from . import models, schemas
import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    # bcrypt chỉ hỗ trợ tối đa 72 ký tự
    password_bytes = plain_password[:72].encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    # bcrypt chỉ hỗ trợ tối đa 72 ký tự
    password_bytes = password[:72].encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def get_user_by_username(db: Session, username: str):
    """Get user by username"""
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate user with username and password"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not user.hashed_password:
        return None  # User registered via SSO, no password
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user (legacy for SSO)"""
    # bcrypt chỉ hỗ trợ tối đa 72 ký tự
    hashed_password = get_password_hash(user.password) if user.password else None
    db_user = models.User(
        username=user.username,
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        provider=user.provider or "local"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def register_user(db: Session, user: schemas.UserRegister):
    """Register a new user with username and password"""
    # Check if username already exists
    if get_user_by_username(db, user.username):
        return None
    # Check if email already exists
    if get_user_by_email(db, user.email):
        return None
    
    # Create new user
    # bcrypt chỉ hỗ trợ tối đa 72 ký tự (xử lý trong get_password_hash)
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        name=user.username,  # Default name to username
        hashed_password=hashed_password,
        provider="local"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
