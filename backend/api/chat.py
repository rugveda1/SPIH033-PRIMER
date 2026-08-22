from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from backend.database import get_db
from backend.models.chat import ChatSession, ChatMessage
from backend.models.concept import Concept
from backend.models.student import Student
from backend.models.mastery import Mastery
from backend.models.attempt import Attempt
from backend.models.question import Question
from backend.schemas.chat import ChatMessageIn, ChatSessionOut, ChatMessageOut, ChatHintIn, ChatExplainIn
from backend.services.auth import get_current_student
from backend.services.grok import call_grok_api
from backend.services.knowledge_graph import KnowledgeGraphService

router = APIRouter(prefix="/api/chat", tags=["Socratic Tutoring Chat"])

def get_session_context(db: Session, student_id: int, concept_id: int) -> dict:
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        return {}

    mastery = db.query(Mastery).filter(
        Mastery.student_id == student_id,
        Mastery.concept_id == concept_id
    ).first()
    mastery_score = mastery.mastery_score if mastery else 0.0

    prereqs = KnowledgeGraphService.get_direct_prerequisites(db, concept_id)
    prereqs_str = ", ".join([f"{p.name}" for p in prereqs]) if prereqs else "None"

    attempts = db.query(Attempt).join(Question).filter(
        Attempt.student_id == student_id,
        Question.concept_id == concept_id,
        Attempt.is_correct == False
    ).order_by(Attempt.created_at.desc()).limit(5).all()
    recent_mistakes = list(set([a.error_type for a in attempts]))

    return {
        "class_level": concept.class_level,
        "concept_name": concept.name,
        "difficulty": concept.difficulty,
        "mastery_score": mastery_score,
        "learning_objectives": concept.learning_objectives,
        "prerequisites": prereqs_str,
        "recent_mistakes": recent_mistakes,
        "recommended_next_step": "Guide the student through basic Socratic examples."
    }

@router.post("", response_model=ChatMessageOut)
def send_chat_message(
    payload: ChatMessageIn,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    session = db.query(ChatSession).filter(
        ChatSession.student_id == current_student.id,
        ChatSession.concept_id == payload.concept_id
    ).first()

    if not session:
        session = ChatSession(
            student_id=current_student.id,
            concept_id=payload.concept_id,
            created_at=datetime.now(timezone.utc)
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    # Log student message
    student_msg = ChatMessage(
        session_id=session.id,
        role="user",
        content=payload.message,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(student_msg)
    db.commit()

    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session.id
    ).order_by(ChatMessage.timestamp.asc()).all()
    
    chat_history = [{"role": m.role, "content": m.content} for m in messages[-10:]]

    context = get_session_context(db, current_student.id, payload.concept_id)

    response_text = call_grok_api(chat_history, context, mode="chat")

    # Log tutor message
    tutor_msg = ChatMessage(
        session_id=session.id,
        role="assistant",
        content=response_text,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(tutor_msg)
    db.commit()
    db.refresh(tutor_msg)

    return tutor_msg

@router.post("/hint")
def request_hint(
    payload: ChatHintIn,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    context = get_session_context(db, current_student.id, payload.concept_id)
    
    user_prompt = "Can you give me a Socratic hint to help me understand how to solve this math topic?"
    if payload.question_id:
        question = db.query(Question).filter(Question.id == payload.question_id).first()
        if question:
            user_prompt = f"I am working on this question: '{question.question_text}'. Can you give me a gentle Socratic hint without revealing the answer?"

    chat_history = [{"role": "user", "content": user_prompt}]
    hint = call_grok_api(chat_history, context, mode="hint")
    
    return {"hint": hint}

@router.post("/explain")
def request_explanation(
    payload: ChatExplainIn,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    context = get_session_context(db, current_student.id, payload.concept_id)
    
    last_incorrect = db.query(Attempt).join(Question).filter(
        Attempt.student_id == current_student.id,
        Question.concept_id == payload.concept_id,
        Attempt.is_correct == False
    ).order_by(Attempt.created_at.desc()).first()

    user_prompt = "Can you explain this math topic to me like I am a beginner?"
    if last_incorrect:
        user_prompt = f"On this topic, I recently got this question wrong: '{last_incorrect.question.question_text}'. I answered '{last_incorrect.submitted_answer}', but that was not correct. Can you explain where my mistake was using error type '{last_incorrect.error_type}'?"

    chat_history = [{"role": "user", "content": user_prompt}]
    explanation = call_grok_api(chat_history, context, mode="explain")
    
    return {"explanation": explanation}

@router.get("/sessions", response_model=List[ChatSessionOut])
def get_chat_sessions(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    sessions = db.query(ChatSession).filter(
        ChatSession.student_id == current_student.id
    ).all()
    return sessions

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageOut])
def get_session_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.student_id == current_student.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
        
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.timestamp.asc()).all()
    
    return messages
