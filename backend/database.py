from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Create engine
DATABASE_URL="postgresql://postgres:db%40366@localhost:5432/boc_bi_platform"
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def execute_query(query, params=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), params or ())
        conn.commit()
        return result

def fetch_all(query, params=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), params or ())
        return result.fetchall()

def fetch_one(query, params=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), params or ())
        return result.fetchone()
