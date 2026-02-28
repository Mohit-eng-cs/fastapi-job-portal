from sqlalchemy import Column,Integer,String,Text
from app.db.base_class import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, Column, Date, ForeignKey, Index , Integer,String,Boolean,Numeric, Text, UniqueConstraint,text



class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=False)
    skills_required = Column(Text, nullable=True)  # keep simple text; can switch to JSONB later
    posted_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    job_code=Column(String,unique=True,nullable=False)
    Min_sal = Column(Integer,unique=False,nullable=True)
    Max_sal = Column(Integer,unique=False,nullable=True)

    recruiter = relationship("User", back_populates="posted_jobs")
    applications = relationship("Application", back_populates="job", cascade="all,delete-orphan")

