from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = 'postgresql+psycopg://postgres:glebik228900@localhost:5432/routecore'

engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()