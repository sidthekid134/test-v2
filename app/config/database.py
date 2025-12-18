from sqlmodel import Session, create_engine

# Database URL
DATABASE_URL = "sqlite:///./test.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

# Session dependency
def get_session():
    with Session(engine) as session:
        yield session