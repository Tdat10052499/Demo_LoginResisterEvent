from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas, crud, database
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from .routes import auth, event

app = FastAPI(title="Login Register Event API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
async def root():
    return {"message": "Welcome to Login Register Event API"}

@app.post("/register", response_model=schemas.UserRead)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

app.include_router(auth.router)
app.include_router(event.router)