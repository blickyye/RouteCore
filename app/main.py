from fastapi import FastAPI

from pathlib import Path

from app.database.database import Base, engine
from app.database import models
from app.auth.router import router as auth_router
from app.couriers.router import router as couriers_router
from app.orders.router import router as orders_router

from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(auth_router, prefix='/app/auth', tags=['Create user'])
app.include_router(couriers_router, prefix='/app/couriers', tags=['Couriers'])
app.include_router(orders_router, prefix='/app/orders', tags=['Orders'])

Base.metadata.create_all(bind=engine)

frontend_dir = Path(__file__).resolve().parent.parent / 'frontend'
app.mount('/', StaticFiles(directory=frontend_dir, html=True), name='frontend')