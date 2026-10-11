from fastapi import FastAPI

from app.database.database import Base, engine
from app.database import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

