from sqlmodel import Session, create_engine
import os



DB_URL = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "ingatlan"

engine = create_engine(f"mysql+mysqldb://{DB_USER}:{DB_PASS}@{DB_URL}/{DB_NAME}", echo=True)


def get_session():
    with Session(engine) as session:
        yield session

def get_session_nodep():
    return Session(engine)