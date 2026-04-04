from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///pottajoe.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Rating(Base):
    __tablename__ = "ratings"

    id          = Column(Integer, primary_key=True, index=True)
    coffee_name = Column(String, index=True)
    user_input  = Column(String)
    stars       = Column(Integer)        # 1–5
    created_at  = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)