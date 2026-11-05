from fastapi import FastAPI
from database import engine
from models import Base
from routes import router as task_router

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app

app = FastAPI()

app.include_router(task_router, prefix="/task", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Service"}