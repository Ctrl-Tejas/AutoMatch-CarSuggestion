from pydantic import BaseModel
from typing import Optional, List

class SurveyCreate(BaseModel):
    name: str
    age_group: str
    city: str
    occupation: Optional[str] = None
    family_size: Optional[int] = None
    
    buying_reason: str
    priority: str
    
    usage_type: str
    driving_area: str
    distance: Optional[str] = None
    
    car_type: str
    fuel_type: str
    transmission: Optional[str] = None
    
    budget: str
    used_car_interest: Optional[str] = None
    
    mileage: int
    safety: int
    tech: int
    comfort: int
    
    ev_interest: str
    additional_preferences: Optional[str] = None
    feedback: Optional[str] = None

class SurveySubmissionResponse(SurveyCreate):
    id: int
    
    class Config:
        from_attributes = True

class CarRecommendation(BaseModel):
    name: str
    match_percentage: int
    reasons: List[str]

class SubmissionResult(BaseModel):
    message: str
    submission_id: int
    recommendations: List[CarRecommendation]
