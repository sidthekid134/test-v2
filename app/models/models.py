from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Database configuration
DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(DATABASE_URL, echo=True)

# Model for "11" implementation
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: str = Field(default="11")
    description: Optional[str] = None

# Create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# CRUD functions
def get_session():
    with Session(engine) as session:
        yield session

def get_items(session: Session):
    statement = select(Item)
    items = session.exec(statement).all()
    return items

def get_item(session: Session, item_id: int):
    statement = select(Item).where(Item.id == item_id)
    item = session.exec(statement).first()
    return item

def create_item(session: Session, item: Item):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

def update_item(session: Session, item_id: int, item: Item):
    db_item = get_item(session, item_id)
    if db_item:
        for key, value in item.dict(exclude_unset=True).items():
            setattr(db_item, key, value)
        session.commit()
        session.refresh(db_item)
    return db_item

def delete_item(session: Session, item_id: int):
    db_item = get_item(session, item_id)
    if db_item:
        session.delete(db_item)
        session.commit()
    return db_item