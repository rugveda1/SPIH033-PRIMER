from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.concept import Concept
from backend.models.student import Student
from backend.schemas.concept import ConceptOut, ConceptReadiness
from backend.services.auth import get_current_student
from backend.services.knowledge_graph import KnowledgeGraphService

router = APIRouter(prefix="/api/concepts", tags=["Concepts & Knowledge Graph"])

@router.get("", response_model=List[ConceptOut])
def get_concepts(class_level: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Concept)
    if class_level is not None:
        query = query.filter(Concept.class_level == class_level)
    return query.all()

@router.get("/{concept_id}", response_model=ConceptOut)
def get_concept(concept_id: int, db: Session = Depends(get_db)):
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Concept with ID {concept_id} not found"
        )
    return concept

@router.get("/{concept_id}/prerequisites", response_model=List[ConceptOut])
def get_prerequisites(concept_id: int, recursive: bool = False, db: Session = Depends(get_db)):
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Concept with ID {concept_id} not found"
        )
    
    if recursive:
        prereq_ids = KnowledgeGraphService.get_recursive_prerequisites(db, concept_id)
        if not prereq_ids:
            return []
        return db.query(Concept).filter(Concept.id.in_(prereq_ids)).all()
    else:
        return KnowledgeGraphService.get_direct_prerequisites(db, concept_id)

@router.get("/{concept_id}/ready", response_model=ConceptReadiness)
def check_readiness(
    concept_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Concept with ID {concept_id} not found"
        )
    
    try:
        readiness = KnowledgeGraphService.get_student_readiness(db, current_student.id, concept_id)
        return readiness
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
