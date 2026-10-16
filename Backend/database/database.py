from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

DB_URL = "sqlite:///./tasks.db"

engine = create_engine(DB_URL,connect_args={"check_same_thread": False})
sessionlocal = sessionmaker(bind=engine)

def get_db():
    with sessionlocal() as db:
        yield db