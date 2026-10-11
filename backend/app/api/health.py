from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database.database import get_db
from backend.app.database.crud import counts
router = APIRouter()
@router.get("")
def health(db: Session = Depends(get_db)):
    return {"status":"healthy","service":"CareerMatch AI","data_counts":counts(db)}
