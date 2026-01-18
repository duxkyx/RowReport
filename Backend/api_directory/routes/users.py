from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from Database.db import get_session
from api_directory.schemas import User, UserLogin
from Database.crud import user_management as crud

router = APIRouter()

# FastAPI register user route
@router.post("/register")
def register(user: User, session: Session = Depends(get_session)):
    try:
        return crud.create_user(session, user)
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
def get_users(session: Session = Depends(get_session)):
    users = crud.get_all_users(session)
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