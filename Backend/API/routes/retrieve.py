from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from Backend.Database.db import get_session
from Backend.API.schemas import BoatTelemetryData, UserTelemetryData
from Backend.Database.crud import telemetry_management as crud

router = APIRouter()

@router.get("/user_data/get_summary/{user_id}")
def get_summary(user_id: int, session: Session = Depends(get_session)):
    summary = crud.get_user_summary(session, user_id)
    if summary is None:
        raise HTTPException(status_code=404, detail="User summary not found")
    return summary

@router.get("/user_data/get_averages/{user_id}")
def get_summary(user_id: int, session: Session = Depends(get_session)):
    summary = crud.get_user_averages(session, user_id)
    if summary is None:
        raise HTTPException(status_code=404, detail="User averages not found")
    return summary

@router.get("/user_data/get_radar_averages/{user_id}")
def get_radar_averages(user_id: int, session: Session = Depends(get_session)):
    radar_averages = crud.get_user_radar_averages(session, user_id)
    if radar_averages is None:
        raise HTTPException(status_code=404, detail="User radar averages not found")
    return radar_averages

@router.get('/user_data/get_telemetry_data/{user_id}')
def get_user_telemetry(user_id: int, session: Session = Depends(get_session)):
    radar_averages = crud.get_user_telemetry_data(session, user_id)
    if radar_averages is None:
        raise HTTPException(status_code=404, detail="User gateforce averages not found")
    return radar_averages

@router.get("/user_data/get_sessions/{user_id}")
def get_sessions(user_id: int, session: Session = Depends(get_session)):
    sessions = crud.get_user_sessions(session, user_id)
    if sessions is None:
        raise HTTPException(status_code=404, detail="User sessions not found")
    return sessions

@router.get("/user_data/get_rower_data/{session_id}")
def get_rower_data(session_id: int, session: Session = Depends(get_session)):
    data = crud.get_rower_data(session, session_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Rower data not found for session")
    return data