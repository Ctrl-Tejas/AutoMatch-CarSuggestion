from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
from database import Base

class SurveySubmission(Base):
    __tablename__ = "survey_submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    age_group = Column(String(50))
    city = Column(String(100))
    occupation = Column(String(100), nullable=True)
    family_size = Column(Integer, nullable=True)

    buying_reason = Column(String(100))
    priority = Column(String(100))

    usage_type = Column(String(100))
    driving_area = Column(String(100))
    distance = Column(String(100), nullable=True)

    car_type = Column(String(100))
    fuel_type = Column(String(100))
    transmission = Column(String(100), nullable=True)

    budget = Column(String(100))
    used_car_interest = Column(String(10), nullable=True)

    mileage = Column(Integer)
    safety = Column(Integer)
    tech = Column(Integer)
    comfort = Column(Integer)

    ev_interest = Column(String(20))
    additional_preferences = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
