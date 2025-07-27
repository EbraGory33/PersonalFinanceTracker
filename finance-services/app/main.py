from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.router import api_router

from app.utils.database import Base, engine

from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


# Lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Creating database tables if they do not exist...")
    Base.metadata.create_all(bind=engine)
    print("Database ready!")
    yield
    # Shutdown logic (optional)
    print("Shutting down FinPilot Core API...")

app = FastAPI(title="FinPilot Core API", lifespan=lifespan)

# Middleware
if settings.MODE == "production":
    origins = [settings.Frontend_Url]  # or load from env
else: 
    origins = [
        "http://localhost:3000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
@app.get("/")
async def root():
    return {"message": "Welcome to FinPilot Core API!"}

app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)