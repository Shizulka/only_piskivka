import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, text
from src.modules.analytics.application.handlers.user_deleted_analytics_handler import UserDeletedAnalyticsHandler
from src.modules.core.application.event.user_event import UserDeletedEvent, UserRegisteredEvent
from src.modules.analytics.application.handlers.user_registered_analytics_handler import UserRegisteredAnalyticsHandler
from src.modules.analytics.application.handlers.review_deleted_analytics_handler import ReviewDeletedAnalyticsHandler
from src.modules.analytics.application.handlers.review_created_analytics_handler import ReviewCreatedAnalyticsHandler
from src.modules.core.application.event.review_event import ReviewCreatedEvent, ReviewDeletedEvent
from src.modules.analytics.application.handlers.place_deleted_analytics_handler import PlaceDeletedAnalyticsHandler
from src.modules.core.application.audit.audit_handlers import PlaceDeletedAuditHandler
from src.modules.core.application.audit.audit_service import ConsoleAuditService
from src.modules.analytics.application.handlers.place_created_analytics_handler import PlaceCreatedAnalyticsHandler
from src.modules.analytics.infrastructure.repository.repo_analytics import AnalyticsRepository
from src.modules.core.application.event.place_event import PlaceCreatedEvent, PlaceDeletedEvent
from src.shared.event_bus import event_bus
from src.modules.core.infrastructure.dependencies import get_current_user
from src.modules.core.infrastructure.models import Base, Users
from src.modules.core.infrastructure.database import get_db
from fastapi import FastAPI
from dotenv import load_dotenv

from src.modules.core.presentation import control_place , control_user ,  control_review

load_dotenv()

app = FastAPI()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app.include_router(control_place.router)
app.include_router(control_user.router)
app.include_router(control_review.router)

Base.metadata.create_all(bind=engine)

def setup_event_subscribers():
    db = SessionLocal()

    analytics_repo = AnalyticsRepository(db)
    review_deleted_handler = ReviewDeletedAnalyticsHandler(analytics_repo)
    place_created_handler = PlaceCreatedAnalyticsHandler(SessionLocal)
    place_deleted_handler = PlaceDeletedAnalyticsHandler(analytics_repo)
    review_created_handler = ReviewCreatedAnalyticsHandler(analytics_repo)
    user_registered_handler = UserRegisteredAnalyticsHandler(analytics_repo)
    user_deleted_handler = UserDeletedAnalyticsHandler(analytics_repo)
    
    event_bus.subscribe(PlaceCreatedEvent, place_created_handler.handle)
    event_bus.subscribe(PlaceDeletedEvent, place_deleted_handler.handle)
    event_bus.subscribe(ReviewCreatedEvent, review_created_handler.handle)
    event_bus.subscribe(ReviewDeletedEvent,review_deleted_handler.handle)
    event_bus.subscribe(UserRegisteredEvent,user_registered_handler.handle)
    event_bus.subscribe(UserDeletedEvent,user_deleted_handler.handle)



setup_event_subscribers()

@app.get("/health")
def health_check(db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "message": "робе"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))