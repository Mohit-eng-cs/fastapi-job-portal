from sqlalchemy import Column,Integer,String,Text
from app.db.base_class import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, Column, Date, ForeignKey, Index , Integer,String,Boolean,Numeric, Text, UniqueConstraint,text

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False, server_default="applied")
    resume_url = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    candidate = relationship("User", backref="applications")
    job = relationship("Job", back_populates="applications")

    __table_args__ = (
        UniqueConstraint("candidate_id", "job_id", name="uq_applications_candidate_job"),
        Index("ix_applications_job_status", "job_id", "status"),
    )


class ApplicationStatusHistory(Base):
    __tablename__ = "application_status_history"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    old_status = Column(String, nullable=True)
    new_status = Column(String, nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    changed_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    application = relationship("Application", backref="status_history")
    actor = relationship("User")
