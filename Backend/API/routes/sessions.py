from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from Backend.Database.db import get_session
from Backend.API.schemas import BoatTelemetryData, UserTelemetryData
from Backend.Database.crud import telemetry_management as crud

router = APIRouter()

@router.post("/upload/session")
def upload_session(boat_data: BoatTelemetryData, session: Session = Depends(get_session)):
    try:
        return crud.add_session(session, boat_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/upload/user_data")
def upload_user_data(rower_data: UserTelemetryData, session: Session = Depends(get_session)):
    try:
        return crud.add_rower_data(session, rower_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete('/delete/session/{session_id}')
def delete_session(session_id: int, session: Session = Depends(get_session)):
    try:
        return crud.delete_session(session, session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))