from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use ./ so it’s relative to project root
DATABASE_URL = "sqlite:///./data.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # only for SQLite
    echo=True,   # show SQL queries
    future=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
