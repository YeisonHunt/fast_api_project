from fastapi import FastAPI
from app.routes import users, items
from app.database import engine
from app.models.models import Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI SQLAlchemy App")

# Include routers
app.include_router(users.router, tags=["users"])
app.include_router(items.router, tags=["items"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI SQLAlchemy App"}