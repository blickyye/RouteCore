from fastapi import FastAPI

from app.database.database import Base, engine
from app.database import models
from app.auth.router import router as auth_router
from app.couriers.router import router as couriers_router
from app.orders.router import router as orders_router

app = FastAPI()

app.include_router(auth_router, prefix='/app/auth', tags=['Create user'])
app.include_router(couriers_router, prefix='/app/couriers', tags=['Couriers'])
app.include_router(orders_router, prefix='/orders', tags=['Orders'])

Base.metadata.create_all(bind=engine)

