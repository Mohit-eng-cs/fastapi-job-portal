from sqlalchemy import Column,Integer,String,Text
from app.db.base_class import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.job import Job
from app.models.applications import Application
from sqlalchemy import TIMESTAMP, Column, Date, ForeignKey, Index , Integer,String,Boolean,Numeric, Text, UniqueConstraint,text

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # store hash
    # merged fields from Registration:
    name = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    location = Column(String, nullable=True)
    exp = Column(String, nullable=True)
    role = Column(String, nullable=False, server_default="candidate")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    posted_jobs = relationship("Job", back_populates="recruiter", cascade="all,delete-orphan")

