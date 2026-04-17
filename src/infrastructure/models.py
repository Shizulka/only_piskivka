from typing import Optional
import datetime
import enum

from sqlalchemy import Enum, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, Text, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class PlaceStatus(str, enum.Enum):
    BAR = 'bar'
    CAFE = 'cafe'
    SHOP = 'shop'


class UserStatus(str, enum.Enum):
    COOL = 'cool'
    SUPER_COOL = 'super cool'
    MEGA_COOL = 'mega cool'


class Place(Base):
    __tablename__ = 'place'
    __table_args__ = (
        PrimaryKeyConstraint('place_id', name='place_pkey'),
    )

    place_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    location: Mapped[str] = mapped_column(String(50), nullable=False)
    open: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    close: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    type_place: Mapped[PlaceStatus] = mapped_column(Enum(PlaceStatus, values_callable=lambda cls: [member.value for member in cls], name='place_status'), nullable=False)

    review: Mapped[list['Review']] = relationship('Review', back_populates='place')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='users_pkey'),
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(100))
    phone_number: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[Optional[UserStatus]] = mapped_column(Enum(UserStatus, values_callable=lambda cls: [member.value for member in cls], name='user_status'))

    review: Mapped[list['Review']] = relationship('Review', back_populates='user')


class Review(Base):
    __tablename__ = 'review'
    __table_args__ = (
        ForeignKeyConstraint(['place_id'], ['place.place_id'], name='review_place_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='review_user_id_fkey'),
        PrimaryKeyConstraint('review_id', name='review_pkey')
    )

    review_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    place_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_in: Mapped[str] = mapped_column(Text, nullable=False)

    place: Mapped['Place'] = relationship('Place', back_populates='review')
    user: Mapped['Users'] = relationship('Users', back_populates='review')
