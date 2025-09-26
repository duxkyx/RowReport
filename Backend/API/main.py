# API Main
from fastapi import FastAPI
from sqlmodel import SQLModel
from Backend.Database.db import engine
from Backend.API.routes import sessions, users, retrieve
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL(s) for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    #SQLModel.metadata.drop_all(engine)

app.include_router(users.router)
app.include_router(sessions.router)
app.include_router(retrieve.router)
