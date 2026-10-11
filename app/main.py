from fastapi import FastAPI

from app.database.database import Base, engine
from app.database import models
from app.auth.router import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix='/app/auth', tags=['Create user'])

Base.metadata.create_all(bind=engine)

