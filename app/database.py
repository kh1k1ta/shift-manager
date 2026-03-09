from sqlalchemy import create_engine, Column, Integer, Text, Boolean, Date, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# --- モデル定義 ---

class Worker(Base):
    __tablename__ = "workers"
    id          = Column(Integer, primary_key=True)
    name        = Column(Text, nullable=False)
    hourly_wage = Column(Integer, nullable=False, default=1036)
    is_active   = Column(Boolean, default=True)


class MonthlyBudget(Base):
    __tablename__ = "monthly_budgets"
    id         = Column(Integer, primary_key=True)
    month      = Column(Date, nullable=False, unique=True)
    budget_yen = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Availability(Base):
    __tablename__ = "availability"
    id           = Column(Integer, primary_key=True)
    worker_id    = Column(Integer, nullable=False)
    date         = Column(Date, nullable=False)
    shift_type   = Column(Text, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())


class ScheduledShift(Base):
    __tablename__ = "scheduled_shifts"
    id               = Column(Integer, primary_key=True)
    worker_id        = Column(Integer, nullable=False)
    date             = Column(Date, nullable=False)
    shift_type       = Column(Text, nullable=False)
    role             = Column(Text, nullable=False)
    backup_priority  = Column(Integer)
    schedule_month   = Column(Date, nullable=False)
    created_at       = Column(DateTime(timezone=True), server_default=func.now())


class ActualAttendance(Base):
    __tablename__ = "actual_attendance"
    id                  = Column(Integer, primary_key=True)
    scheduled_shift_id  = Column(Integer, nullable=False)
    attended            = Column(Boolean)
    note                = Column(Text)
    recorded_at         = Column(DateTime(timezone=True), server_default=func.now())


class ChangeRequest(Base):
    __tablename__ = "change_requests"
    id           = Column(Integer, primary_key=True)
    worker_id    = Column(Integer, nullable=False)
    date         = Column(Date, nullable=False)
    shift_type   = Column(Text, nullable=False)
    reason       = Column(Text)
    status       = Column(Text, default="pending")
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
