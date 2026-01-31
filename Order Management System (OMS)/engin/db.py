from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from engin.Base import BASE
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL", "sqlite:///oms.db")

engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    # Import models to ensure they are registered with BASE
    from models import User, Order, Plate
    BASE.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
