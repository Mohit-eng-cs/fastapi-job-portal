from app.db.sessions import engine
from app.db.base import Base

# ⭐ IMPORTANT: Import every model so SQLAlchemy registers them
from app.models.user import User
from app.models.job import Job
from app.models.applications import Application, ApplicationStatusHistory

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
