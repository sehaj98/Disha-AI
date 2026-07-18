from datetime import date
from sqlalchemy import Column, Integer, String, Date, JSON

from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=True)

    country = Column(String, nullable=True)
    current_class = Column(Integer, nullable=True)
    interests = Column(JSON, default=list)

    # Used by the weekly promotion job: if today has passed the next
    # academic-year boundary since this date, current_class gets bumped by 1.
    last_promoted_date = Column(Date, default=date.today)

    # Used by the email scheduler: null means "never emailed yet".
    last_emailed_at = Column(Date, nullable=True)

    created_at = Column(Date, default=date.today)
    