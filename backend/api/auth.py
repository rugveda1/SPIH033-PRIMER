from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.student import Student
from backend.schemas.auth import StudentSignUp, StudentLogin, Token, StudentOut
from backend.services.auth import hash_password, verify_password, create_access_token, get_current_student

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/signup", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def signup(student_data: StudentSignUp, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == student_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed = hash_password(student_data.password)
    student = Student(
        name=student_data.name,
        email=student_data.email,
        password_hash=hashed,
        class_level=student_data.class_level
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Standard OAuth2 Form post (used by Swagger)
    student = db.query(Student).filter(Student.email == form_data.username).first()
    if not student or not verify_password(form_data.password, student.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": student.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login-json", response_model=Token)
def login_json(login_data: StudentLogin, db: Session = Depends(get_db)):
    # JSON body post helper (convenient for API clients/JS integrations)
    student = db.query(Student).filter(Student.email == login_data.email).first()
    if not student or not verify_password(login_data.password, student.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token = create_access_token(data={"sub": student.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=StudentOut)
def read_users_me(current_student: Student = Depends(get_current_student)):
    return current_student

class ProfileUpdateIn(BaseModel):
    name: str | None = None
    class_level: int | None = None

@router.put("/profile", response_model=StudentOut)
def update_profile(
    payload: ProfileUpdateIn,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    if payload.name is not None:
        current_student.name = payload.name
    if payload.class_level is not None:
        current_student.class_level = payload.class_level
    db.commit()
    db.refresh(current_student)
    return current_student

from backend.models.mastery import Mastery
from backend.models.attempt import Attempt
from backend.models.assessment import Assessment
from backend.models.concept import Concept
from backend.models.question import Question
from backend.services.adaptive_engine import AdaptiveEngineService

@router.get("/me/progress")
def get_my_progress(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    # Fetch concepts for this class
    concepts = db.query(Concept).filter(Concept.class_level == current_student.class_level).all()
    concept_ids = [c.id for c in concepts]

    # Fetch mastery records
    mastery_records = db.query(Mastery).filter(
        Mastery.student_id == current_student.id,
        Mastery.concept_id.in_(concept_ids)
    ).all()
    mastery_map = {m.concept_id: m.mastery_score for m in mastery_records}

    # Calculate average mastery score
    total_score = 0.0
    for c in concepts:
        total_score += mastery_map.get(c.id, 0.0)
    overall_mastery = (total_score / len(concepts)) if concepts else 0.0

    # Concept mastery breakdown, strengths and weaknesses
    concept_mastery = []
    strengths = []
    weaknesses = []
    for c in concepts:
        score = mastery_map.get(c.id, 0.0)
        c_info = {"id": c.id, "name": c.name, "score": score}
        concept_mastery.append(c_info)
        if score >= 80.0:
            strengths.append(c_info)
        else:
            weaknesses.append(c_info)

    # Recent mistakes (last 20 attempts)
    recent_attempts = db.query(Attempt).filter(
        Attempt.student_id == current_student.id
    ).order_by(Attempt.created_at.desc()).limit(20).all()
    
    recent_mistakes = []
    for a in recent_attempts:
        if not a.is_correct and a.error_type != "unknown" and a.error_type not in recent_mistakes:
            recent_mistakes.append(a.error_type)

    # Completed assessments
    completed_assessments = db.query(Assessment).filter(
        Assessment.student_id == current_student.id
    ).order_by(Assessment.created_at.desc()).all()
    assessments_list = [
        {
            "id": ass.id,
            "assessment_type": ass.assessment_type,
            "score": ass.score,
            "created_at": str(ass.created_at)
        }
        for ass in completed_assessments
    ]

    # Recommended next topic
    rec_concept = AdaptiveEngineService.recommend_next_concept(db, current_student.id, current_student.class_level)
    recommended_topic = {
        "id": rec_concept.id,
        "name": rec_concept.name,
        "description": rec_concept.description
    } if rec_concept else None

    # Learning history (last 10 attempts joined with questions and concepts)
    history_records = db.query(Attempt).join(Question).filter(
        Attempt.student_id == current_student.id
    ).order_by(Attempt.created_at.desc()).limit(10).all()
    
    learning_history = [
        {
            "id": h.id,
            "question_text": h.question.question_text,
            "concept_name": h.question.concept.name,
            "is_correct": h.is_correct,
            "score": h.score,
            "error_type": h.error_type,
            "created_at": str(h.created_at)
        }
        for h in history_records
    ]

    return {
        "overall_mastery": overall_mastery,
        "concept_mastery": concept_mastery,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recent_mistakes": recent_mistakes,
        "completed_assessments": assessments_list,
        "recommended_next_topic": recommended_topic,
        "learning_history": learning_history
    }
