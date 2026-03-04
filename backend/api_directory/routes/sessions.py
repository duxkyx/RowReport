from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session
from database_directory.db import get_session
from api_directory.schemas import BoatTelemetryData, UserTelemetryData, CoxswainData
from database_directory.crud import telemetry_management as crud
from api_directory import send_email

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
    
@router.post("/upload/coxswain_data")
def upload_coxswain_data(coxswain_data: CoxswainData, session: Session = Depends(get_session)):
    try:
        return crud.add_coxswain_data(session, coxswain_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete('/delete/session/{session_id}')
def delete_session(session_id: int, session: Session = Depends(get_session)):
    try:
        return crud.delete_session(session, session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/update/assign_rower')
def assign_rower(payload: dict, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    """Payload: {"session_id": int, "seat": int, "user_id": int or null}"""
    try:
        session_id = payload.get('session_id')
        seat = payload.get('seat')
        user_id = payload.get('user_id')
        if session_id is None or seat is None:
            raise HTTPException(status_code=400, detail='session_id and seat are required')

        updated = crud.update_rower_assignment(session, int(session_id), int(seat), int(user_id) if user_id is not None else None)
        if not updated:
            raise HTTPException(status_code=404, detail='Row not found')

        # Send email notification to the newly assigned user (if any)
        if user_id is not None:
            background_tasks.add_task(send_email.send_telemetry_email, payload.get('boat_data', {}), int(user_id), int(session_id), session)

        return {'message': 'Assignment updated'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/update/assign_coxswain')
def assign_coxswain(payload: dict, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    """Payload: {"session_id": int, "coxswain_id": int or null}"""
    try:
        session_id = payload.get('session_id')
        coxswain_id = payload.get('coxswain_id')
        if session_id is None:
            raise HTTPException(status_code=400, detail='session_id is required')

        updated = crud.update_coxswain(session, int(session_id), int(coxswain_id) if coxswain_id is not None else None)

        if coxswain_id is not None:
            background_tasks.add_task(send_email.send_telemetry_email, payload.get('boat_data', {}), int(coxswain_id), int(session_id), session)

        return {'message': 'Coxswain updated'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))