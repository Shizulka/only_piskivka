from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, text
from src.infrastructure.database import get_db, db_ping
from fastapi import FastAPI

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:1@127.0.0.1:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def db_ping(db: Session) -> None:
    db.execute(text("SELECT 1"))

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "message": "робе"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))