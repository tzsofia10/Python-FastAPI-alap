from sqlmodel import Session, create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DB_URL")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"mysql+mysqldb://{DB_USER}:{DB_PASS}@{DB_URL}/{DB_NAME}", echo=True)


def get_session():
    with Session(engine) as session:
        yield session

def get_session_nodep():
    return Session(engine)