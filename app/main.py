from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.items import router as items_router
from app.routes.users import router as users_router
from app.models.models import Base
# Fix the import to use the app.database module
from app.database import engine

# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Energy Billing API",
    description="API for calculating and analyzing energy billing",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(items_router, prefix="/api/v1", tags=["Energy Billing"])
app.include_router(users_router, prefix="/api/v1", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Energy Billing API"}