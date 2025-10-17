from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, schemas

router = APIRouter(
    prefix="/event",
    tags=["event"]
)

@router.post("/register")
def register_event(event: schemas.EventCreate, db: Session = Depends(database.get_db)):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return {"message": "Đăng ký thành công!", "event_id": db_event.id}

@router.get("/registrations")
def list_registrations(db: Session = Depends(database.get_db)):
    return db.query(models.Event).all()
