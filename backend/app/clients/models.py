from sqlalchemy import Column, Integer, Text, Date, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    counselor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    dob = Column(Date)
    primary_diagnosis = Column(Text)
    primary_concerns = Column(Text)
    therapy_focus = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
