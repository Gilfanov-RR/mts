from sqlalchemy import create_engine, Column, Integer, String, Text, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import json

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Memory(Base):
    __tablename__ = "memories"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    key = Column(String)
    value = Column(Text)
    metadata = Column(JSON)

Base.metadata.create_all(engine)

def get_relevant_memory(user_id: str, query: str, limit=5):
    session = Session()
    rows = session.query(Memory).filter(Memory.user_id == user_id).limit(limit).all()
    session.close()
    return "\n".join([f"{r.key}: {r.value}" for r in rows])

def save_memory(user_id: str, key: str, value: str, metadata=None):
    session = Session()
    m = Memory(user_id=user_id, key=key, value=value, metadata=metadata or {})
    session.add(m)
    session.commit()
    session.close()
