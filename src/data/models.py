# src/data/models.py

from sqlalchemy import Column, String, Integer, Text, DateTime, Date, ForeignKey
from sqlalchemy.types import JSON, BLOB
from sqlalchemy.sql import func
from .database import Base

class LogEntry(Base):
    __tablename__ = "log_table"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    log_type = Column(String, nullable=False)             # log, mood, acc, thank, etc.
    cog_state = Column(String, nullable=True)             # Act, Obs, Crt, Mtn
    comment = Column(Text, nullable=False)
    energy_score = Column(Integer, nullable=True)         # -2 to +2
    emotion_label = Column(String, nullable=True)
    archetype = Column(String, nullable=True)
    tags = Column(String, nullable=True)                  # optional comma-separated tags
    log_time = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    log_day = Column(Date, nullable=False, server_default=func.current_date())
    embedding = Column(BLOB, nullable=True)
    metadta = Column(JSON, nullable=True)
    evnttrigger = Column(String, nullable=True)
    daily_routine = Column(Integer, nullable=True)

class MoodSwing(Base):
    __tablename__ = "swing_table"

    swing_id = Column(String, primary_key=True)
    user_id = Column(Integer, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    energy_path = Column(Text, nullable=False)             # e.g., 0 -> + -> - -> 0
    swing_intensity = Column(Integer, nullable=True)       # max |energy_score|
    swing_volatility = Column(Integer, nullable=True)      # number of non-zero transitions
    log_ids = Column(String, nullable=True)                # comma-separated log_ids
    tags = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
# ORM models