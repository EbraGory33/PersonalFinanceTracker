from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings  # Import settings from config.py

# 🔹 PostgreSQL Configuration (Historical Data)

engine = create_engine(settings.postgres_database_url, echo=True)  # Use the postgres_database_url property from Settings
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)



Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to create tables
def create_db():
    Base.metadata.create_all(bind=engine)
