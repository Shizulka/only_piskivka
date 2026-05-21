from sqlalchemy import Column, Integer, String
from src.modules.core.infrastructure.database import Base


class PlaceStatisticsModel(Base):
    __tablename__ = "place_statistics"

    id = Column(Integer, primary_key=True, index=True)

    external_place_id = Column(Integer, nullable=False)

    location = Column(String, nullable=False)

    status = Column(String, nullable=False)

    total_reviews = Column(Integer, default=0)


class UserStatisticsModel(Base):
    __tablename__ = "user_statistics"

    id = Column(Integer, primary_key=True, index=True)
    total_users = Column(Integer, default=0)