from sqlmodel import Session, SQLModel, create_engine
import os

# Use SQLite for simplicity
DATABASE_URL = "sqlite:///./eleven.db"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session