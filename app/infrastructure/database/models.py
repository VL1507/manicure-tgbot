import datetime

from typing import List, Optional

from sqlalchemy import ForeignKey, Integer, String, TIMESTAMP, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Activities(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)

    mood_activities: Mapped[List["MoodActivities"]] = relationship(
        "MoodActivities", back_populates="activities"
    )


class Emotions(Base):
    __tablename__ = "emotions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    color_hex: Mapped[str] = mapped_column(String)

    mood_emotions: Mapped[List["MoodEmotions"]] = relationship(
        "MoodEmotions", back_populates="emotion"
    )


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    create_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP)

    mood: Mapped[List["Mood"]] = relationship("Mood", back_populates="user")


class Mood(Base):
    __tablename__ = "mood"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    score: Mapped[int] = mapped_column(Integer)
    create_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP)
    update_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP)
    note: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped["User"] = relationship("User", back_populates="mood")
    mood_activities: Mapped[List["MoodActivities"]] = relationship(
        "MoodActivities", back_populates="mood"
    )
    mood_emotions: Mapped[List["MoodEmotions"]] = relationship(
        "MoodEmotions", back_populates="mood"
    )


class MoodActivities(Base):
    __tablename__ = "mood_activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    activities_id: Mapped[int] = mapped_column(ForeignKey("activities.id"))
    mood_id: Mapped[int] = mapped_column(ForeignKey("mood.id"))

    activities: Mapped["Activities"] = relationship(
        "Activities", back_populates="mood_activities"
    )
    mood: Mapped["Mood"] = relationship("Mood", back_populates="mood_activities")


class MoodEmotions(Base):
    __tablename__ = "mood_emotions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    emotion_id: Mapped[int] = mapped_column(ForeignKey("emotions.id"))
    mood_id: Mapped[int] = mapped_column(ForeignKey("mood.id"))

    emotion: Mapped["Emotions"] = relationship(
        "Emotions", back_populates="mood_emotions"
    )
    mood: Mapped["Mood"] = relationship("Mood", back_populates="mood_emotions")
