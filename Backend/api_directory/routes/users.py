from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session
from database_directory.db import get_session
from api_directory.schemas import User, UserLogin, BoatTelemetryData
from database_directory.crud import user_management as crud
from api_directory import send_email
from typing import Optional

router = APIRouter()

# FastAPI register user route
@router.post("/register")
def register(user: User, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    try:
        created_user = crud.create_user(session, user)

        email = created_user.email
        first_name = created_user.first_name
        # Send account confirmation email
        background_tasks.add_task(
            send_email.send_account_confirmation_email, 
            email,
            first_name
        )

        return created_user

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# FastAPI login user route
@router.get("/login")
def login(user: UserLogin, session: Session = Depends(get_session)):
    user = crud.authenticate_user(session, user)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

# FastAPI get all users route
@router.get("/get_all_users")
def get_users(order: Optional[str] = None, session: Session = Depends(get_session)):
    users = crud.get_all_users(session, order)
    if users is None:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# FastAPI delete user route
@router.delete('/delete/user/{user_id}')
def delete_user(user_id: int, session: Session = Depends(get_session)):
    try:
        return crud.delete_user(session, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# FastAPI Email user of telemetry upload
@router.post("/email_user")
def email_user(payload: dict, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    try:
        user_id = payload.get("user_id")
        boat_data = payload.get("boat_data")
        session_id = payload.get("session_id")

        if not boat_data:
            raise HTTPException(status_code=400, detail="boat_data is required")
        
        # Schedule the email to be sent in the background
        background_tasks.add_task(send_email.send_telemetry_email, boat_data, user_id, session_id, session)

        return {"message": "Email sending scheduled"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))