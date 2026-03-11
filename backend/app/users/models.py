from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    role = Column(Text, nullable=False)
    first_name = Column(Text)
    last_name = Column(Text)
    status = Column(Text, nullable=False, default="active")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())