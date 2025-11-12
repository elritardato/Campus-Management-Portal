import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Get the base directory (backend folder)
BASE_DIR = Path(__file__).resolve().parent.parent

# Get DATABASE_URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL")

# Handle relative SQLite paths
if DATABASE_URL and DATABASE_URL.startswith("sqlite:///./"):
    # Extract filename from relative path
    db_filename = DATABASE_URL.replace("sqlite:///./", "")
    # Create full path in backend directory
    db_path = BASE_DIR / db_filename
    # Ensure parent directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    # Update DATABASE_URL to absolute path
    DATABASE_URL = f"sqlite:///{db_path}"
elif not DATABASE_URL:
    # Fallback if no DATABASE_URL is set
    db_path = BASE_DIR / "db.sqlite3"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    DATABASE_URL = f"sqlite:///{db_path}"

# Print database location for debugging
print(f"Using database: {DATABASE_URL}")

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency for getting database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
