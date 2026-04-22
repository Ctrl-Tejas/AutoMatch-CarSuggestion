import csv
import os
import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from dotenv import load_dotenv

# Load environment variables at the entry point
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

from database import engine, get_db, Base
import models, schemas, recommendation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("server.log")
    ]
)
logger = logging.getLogger(__name__)

# Create tables automatically on startup
try:
    models.Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified/created.")
except Exception as e:
    logger.error(f"Error initializing database: {e}")

app = FastAPI(title="AutoMatch India - Used Car Recommendation API")

# More permissive CORS for local dev environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again later."}
    )

@app.post("/api/submit-survey", response_model=schemas.SubmissionResult)
def submit_survey(survey: schemas.SurveyCreate, db: Session = Depends(get_db)):
    logger.info(f"Received survey submission from {survey.name}")
    try:
        # Calculate recommendations
        top_cars = recommendation.recommend_cars(survey)
        
        # Create DB entry
        db_submission = models.SurveySubmission(**survey.dict())
        db.add(db_submission)
        db.commit()
        db.refresh(db_submission)
        
        # Store in CSV as well (configurable directory)
        data_dir = os.getenv("DATA_DIR", "data")
        csv_name = os.getenv("CSV_FILENAME", "survey_submissions.csv")
        os.makedirs(data_dir, exist_ok=True)
        csv_path = os.path.join(data_dir, csv_name)
        
        file_exists = os.path.isfile(csv_path)
        data_dict = survey.dict()
        data_dict['id'] = db_submission.id
        
        with open(csv_path, mode='a', newline='', encoding='utf-8') as f:
            fieldnames = list(data_dict.keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data_dict)
        
        logger.info(f"Successfully processed submission {db_submission.id}")
        return {
            "message": "Survey submitted successfully",
            "submission_id": db_submission.id,
            "recommendations": top_cars
        }
    except Exception as e:
        logger.error(f"Error processing survey: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to process survey submission")

@app.get("/api/admin/analytics")
def get_analytics(db: Session = Depends(get_db)):
    try:
        submissions = db.query(models.SurveySubmission).all()
        
        budget_counts = {}
        fuel_counts = {}
        
        for s in submissions:
            budget_counts[s.budget] = budget_counts.get(s.budget, 0) + 1
            fuel_counts[s.fuel_type] = fuel_counts.get(s.fuel_type, 0) + 1
            
        all_data = [
            {
                "id": s.id,
                "name": s.name,
                "budget": s.budget,
                "fuel_type": s.fuel_type,
                "car_type": s.car_type,
                "created_at": s.created_at.isoformat() if s.created_at else None
            } for s in submissions
        ]
            
        return {
            "budget_distribution": budget_counts,
            "fuel_popularity": fuel_counts,
            "recent_submissions": sorted(all_data, key=lambda x: x["created_at"], reverse=True)[:10]
        }
    except Exception as e:
        logger.error(f"Error fetching analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics data")
