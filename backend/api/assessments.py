import random
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.assessment import Assessment, AssessmentQuestion
from backend.models.question import Question
from backend.models.concept import Concept
from backend.models.student import Student
from backend.models.mastery import Mastery
from backend.schemas.assessment import (
    AssessmentStartIn,
    AssessmentStartOut,
    AssessmentQuestionResponse,
    AssessmentSubmitIn,
    AssessmentSubmitOut,
    AssessmentQuestionResult,
)
from backend.services.auth import get_current_student
from backend.services.mastery import MasteryService
from backend.api.practice import create_dynamic_fallback_question

router = APIRouter(prefix="/api/assessments", tags=["Assessments"])

@router.post("/start", response_model=AssessmentStartOut)
def start_assessment(
    payload: AssessmentStartIn,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    concepts_ids = []
    if payload.assessment_type == "topic":
        if not payload.concept_id:
            raise HTTPException(status_code=400, detail="concept_id is required for topic tests")
        concepts_ids = [payload.concept_id]
    else:
        concepts = db.query(Concept).filter(Concept.class_level == current_student.class_level).all()
        concepts_ids = [c.id for c in concepts]

    questions = db.query(Question).filter(Question.concept_id.in_(concepts_ids)).all()
    
    selected_questions = []
    if len(questions) >= 5:
        selected_questions = random.sample(questions, 5)
    else:
        selected_questions = list(questions)
        needed = 5 - len(selected_questions)
        
        concepts_pool = db.query(Concept).filter(Concept.id.in_(concepts_ids)).all()
        if not concepts_pool:
            concepts_pool = db.query(Concept).all()
            
        for i in range(needed):
            comp = random.choice(concepts_pool)
            q_dict = create_dynamic_fallback_question(comp.id, comp.name, comp.class_level)
            q_dict["id"] = 2000 + comp.id + i
            temp_q = Question(
                id=q_dict["id"],
                concept_id=q_dict["concept_id"],
                class_level=q_dict["class_level"],
                difficulty=q_dict["difficulty"],
                question_type=q_dict["question_type"],
                question_text=q_dict["question_text"],
                options=q_dict["options"],
                correct_answer=q_dict["correct_answer"],
                explanation=q_dict["explanation"]
            )
            db.add(temp_q)
            selected_questions.append(temp_q)

    # Save Assessment instance
    assessment = Assessment(
        student_id=current_student.id,
        assessment_type=payload.assessment_type,
        score=0.0,
        created_at=datetime.now(timezone.utc)
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    # Create AssessmentQuestion mapping rows
    for sq in selected_questions:
        aq = AssessmentQuestion(
            assessment_id=assessment.id,
            question_id=sq.id,
            student_answer=None,
            is_correct=None
        )
        db.add(aq)
    db.commit()

    out_qs = [
        AssessmentQuestionResponse(
            id=sq.id,
            question_text=sq.question_text,
            options=sq.options
        )
        for sq in selected_questions
    ]

    return AssessmentStartOut(
        assessment_id=assessment.id,
        assessment_type=payload.assessment_type,
        questions=out_qs
    )

@router.post("/{assessment_id}/submit", response_model=AssessmentSubmitOut)
def submit_assessment(
    assessment_id: int,
    payload: AssessmentSubmitIn,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id,
        Assessment.student_id == current_student.id
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    answer_map = {ans.question_id: ans.submitted_answer for ans in payload.answers}

    aq_records = db.query(AssessmentQuestion).filter(
        AssessmentQuestion.assessment_id == assessment_id
    ).all()

    correct_count = 0
    total_count = len(aq_records)
    results = []

    for aq in aq_records:
        question = db.query(Question).filter(Question.id == aq.question_id).first()
        if not question:
            concept_id = aq.question_id - 2000
            if concept_id > 2000:
                concept_id %= 50
            concept = db.query(Concept).filter(Concept.id == concept_id).first()
            if not concept:
                concept = db.query(Concept).first()
            q_dict = create_dynamic_fallback_question(concept.id, concept.name, concept.class_level)
            question = Question(
                id=aq.question_id,
                concept_id=concept.id,
                class_level=concept.class_level,
                difficulty=q_dict["difficulty"],
                question_type=q_dict["question_type"],
                question_text=q_dict["question_text"],
                options=q_dict["options"],
                correct_answer=q_dict["correct_answer"],
                explanation=q_dict["explanation"]
            )
            db.add(question)

        submitted = answer_map.get(question.id, "")
        is_correct = question.correct_answer.strip().lower() == submitted.strip().lower()

        aq.student_answer = submitted
        aq.is_correct = is_correct

        if is_correct:
            correct_count += 1

        # Submit to mastery calculations
        MasteryService.evaluate_and_update_mastery(db, current_student.id, question.id, submitted)

        results.append(AssessmentQuestionResult(
            question_id=question.id,
            question_text=question.question_text,
            submitted_answer=submitted,
            correct_answer=question.correct_answer,
            is_correct=is_correct,
            explanation=question.explanation
        ))

    score = (correct_count / total_count * 100.0) if total_count > 0 else 0.0
    assessment.score = score
    db.commit()

    return AssessmentSubmitOut(
        assessment_id=assessment_id,
        score=score,
        results=results
    )
