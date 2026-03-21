from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.sessions import engine
from app import models
from app.api import Job_routes,user_routes,resume_route
import os


app = FastAPI(
    title="CareerPro API",
    description="Backend for job tracking system",
    version="1.0.0"
)

UPLOAD_FOLDER = "uploads"


# CORS (allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER,exist_ok=True)

# Default route (health check)
@app.get("/")
def root():
    return {"message": "CareerPro API is running 🚀"}

# Include Routers
app.include_router(Job_routes.router)
app.include_router(user_routes.router)
app.include_router(resume_route.router)