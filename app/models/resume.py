from sqlalchemy import Column,Integer,String,Text
from app.db.base_class import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.job import Job
from app.models.applications import Application
from sqlalchemy import TIMESTAMP, Column, Date, ForeignKey, Index , Integer,String,Boolean,Numeric, Text, UniqueConstraint,text



class Resume(Base):
    __tablename__ = "resumes"
    id= Column(Integer, primary_key=True,index=True)
    application_id = Column(Integer,ForeignKey("applications.id",ondelete="CASCADE"),nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String, nullable=False)
    uploaded_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    application = relationship("Application", backref="resumes")
