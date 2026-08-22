from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.student import Student
from backend.schemas.concept import ConceptOut
from backend.services.auth import get_current_student
from backend.services.adaptive_engine import AdaptiveEngineService

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("/next", response_model=ConceptOut)
def get_next_recommendation(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    concept = AdaptiveEngineService.recommend_next_concept(db, current_student.id, current_student.class_level)
    if not concept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No recommended concept found for this class level."
        )
    return concept
