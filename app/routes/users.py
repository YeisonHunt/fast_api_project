from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Fix the import to use app.database
from app.database import get_db
from app.models.models import Service

router = APIRouter()

@router.get("/users/{client_id}")
def read_user(client_id: int, db: Session = Depends(get_db)):
    """
    Get basic information about a client (service).
    """
    service = db.query(Service).filter(Service.id_service == client_id).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return {
        "client_id": service.id_service,
        "market_id": service.id_market,
        "voltage_level": service.voltage_level
    }