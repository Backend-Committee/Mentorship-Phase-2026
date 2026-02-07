from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

DATAVBASE_URL = 'sqlite:///data/mydatabase.db'

engine = create_engine(DATAVBASE_URL, echo=True)

Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)