import json
import random
from datetime import datetime, timezone
from fastmcp import FastMCP

from backend.database import SessionLocal
from backend.models.student import Student
from backend.models.concept import Concept
from backend.models.mastery import Mastery
from backend.models.question import Question
from backend.models.attempt import Attempt
from backend.services.knowledge_graph import KnowledgeGraphService
from backend.services.mastery import MasteryService
from backend.services.adaptive_engine import AdaptiveEngineService
from backend.api.practice import create_dynamic_fallback_question

mcp = FastMCP("MathTutorMCP")

@mcp.tool()
def get_student_profile(student_id: int) -> str:
    """Get the student's profile details including name, email, and class level."""
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return f"Error: Student with ID {student_id} not found."
        return json.dumps({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "class_level": student.class_level,
            "created_at": str(student.created_at)
        })
    finally:
        db.close()

@mcp.tool()
def get_concept(concept_id: int) -> str:
    """Get mathematical concept details by ID."""
    db = SessionLocal()
    try:
        concept = db.query(Concept).filter(Concept.id == concept_id).first()
        if not concept:
            return f"Error: Concept with ID {concept_id} not found."
        return json.dumps({
            "id": concept.id,
            "name": concept.name,
            "description": concept.description,
            "class_level": concept.class_level,
            "difficulty": concept.difficulty,
            "learning_objectives": concept.learning_objectives
        })
    finally:
        db.close()

@mcp.tool()
def get_prerequisites(concept_id: int) -> str:
    """Get direct and indirect prerequisites for a concept ID."""
    db = SessionLocal()
    try:
        direct = KnowledgeGraphService.get_direct_prerequisites(db, concept_id)
        recursive = KnowledgeGraphService.get_recursive_prerequisites(db, concept_id)
        return json.dumps({
            "concept_id": concept_id,
            "direct_prerequisites": [p.id for p in direct],
            "recursive_prerequisite_ids": list(recursive)
        })
    finally:
        db.close()

@mcp.tool()
def get_mastery(student_id: int, concept_id: int) -> str:
    """Get student's mastery score and stats for a concept."""
    db = SessionLocal()
    try:
        mastery = db.query(Mastery).filter(
            Mastery.student_id == student_id,
            Mastery.concept_id == concept_id
        ).first()
        if not mastery:
            return json.dumps({
                "student_id": student_id,
                "concept_id": concept_id,
                "mastery_score": 0.0,
                "questions_attempted": 0,
                "questions_correct": 0,
                "confidence": 0.0,
                "last_attempt": None
            })
        return json.dumps({
            "student_id": student_id,
            "concept_id": concept_id,
            "mastery_score": mastery.mastery_score,
            "questions_attempted": mastery.questions_attempted,
            "questions_correct": mastery.questions_correct,
            "confidence": mastery.confidence,
            "last_attempt": str(mastery.last_attempt) if mastery.last_attempt else None
        })
    finally:
        db.close()

@mcp.tool()
def get_weak_topics(student_id: int) -> str:
    """Get list of unmastered or low scoring topics for a student."""
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return f"Error: Student with ID {student_id} not found."
        
        concepts = db.query(Concept).filter(Concept.class_level == student.class_level).all()
        mastery_records = db.query(Mastery).filter(Mastery.student_id == student_id).all()
        mastery_map = {m.concept_id: m.mastery_score for m in mastery_records}
        
        weak = []
        for c in concepts:
            score = mastery_map.get(c.id, 0.0)
            if score < 80.0:
                weak.append({
                    "id": c.id,
                    "name": c.name,
                    "mastery_score": score
                })
        return json.dumps(weak)
    finally:
        db.close()

@mcp.tool()
def get_learning_context(student_id: int, concept_id: int) -> str:
    """Get rich context for teaching: concept, prerequisites, mastery, error patterns, and next steps."""
    db = SessionLocal()
    try:
        concept = db.query(Concept).filter(Concept.id == concept_id).first()
        if not concept:
            return f"Error: Concept with ID {concept_id} not found."
            
        mastery = db.query(Mastery).filter(
            Mastery.student_id == student_id,
            Mastery.concept_id == concept_id
        ).first()
        current_mastery = mastery.mastery_score if mastery else 0.0
        
        direct_prereqs = KnowledgeGraphService.get_direct_prerequisites(db, concept_id)
        prereq_mastery = []
        for p in direct_prereqs:
            pm = db.query(Mastery).filter(
                Mastery.student_id == student_id,
                Mastery.concept_id == p.id
            ).first()
            prereq_mastery.append({
                "concept_id": p.id,
                "name": p.name,
                "mastery_score": pm.mastery_score if pm else 0.0
            })
            
        # Error history
        attempts = db.query(Attempt).join(Question).filter(
            Attempt.student_id == student_id,
            Question.concept_id == concept_id,
            Attempt.is_correct == False
        ).order_by(Attempt.created_at.desc()).limit(5).all()
        recent_errors = list(set([a.error_type for a in attempts]))
        
        # Next recommended topic
        rec_concept = AdaptiveEngineService.recommend_next_concept(db, student_id, concept.class_level)
        rec_context = f"Recommended next concept: {rec_concept.name}" if rec_concept else "No recommendations."
        
        return json.dumps({
            "concept": {
                "id": concept.id,
                "name": concept.name,
                "class_level": concept.class_level,
                "difficulty": concept.difficulty
            },
            "prerequisites": [p.id for p in direct_prereqs],
            "prerequisite_mastery": prereq_mastery,
            "current_mastery": current_mastery,
            "recent_errors": recent_errors,
            "recommendation_context": rec_context
        })
    finally:
        db.close()

@mcp.tool()
def generate_question(concept_id: int, difficulty: str, type: str) -> str:
    """Generate a question for the concept matching difficulty and type constraints."""
    db = SessionLocal()
    try:
        concept = db.query(Concept).filter(Concept.id == concept_id).first()
        if not concept:
            return f"Error: Concept with ID {concept_id} not found."
            
        questions = db.query(Question).filter(
            Question.concept_id == concept_id,
            Question.difficulty == difficulty,
            Question.question_type == type
        ).all()
        
        if questions:
            q = random.choice(questions)
        else:
            # Revert to math dynamic fallback question
            q_dict = create_dynamic_fallback_question(concept_id, concept.name, concept.class_level)
            q = Question(
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
            
        return json.dumps({
            "id": q.id,
            "concept_id": q.concept_id,
            "difficulty": q.difficulty,
            "question_type": q.question_type,
            "question_text": q.question_text,
            "options": q.options,
            "correct_answer": q.correct_answer,
            "explanation": q.explanation
        })
    finally:
        db.close()

@mcp.tool()
def evaluate_answer(question_id: int, student_answer: str, student_id: int = 1) -> str:
    """Evaluate correctness of student answer, logs the attempt, and updates concept mastery score."""
    db = SessionLocal()
    try:
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            concept_id = question_id - 1000 if question_id > 1000 else 1
            concept = db.query(Concept).filter(Concept.id == concept_id).first()
            if not concept:
                concept = db.query(Concept).first()
            q_dict = create_dynamic_fallback_question(concept.id, concept.name, concept.class_level)
            question = Question(
                id=question_id,
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

        attempt = MasteryService.evaluate_and_update_mastery(db, student_id, question.id, student_answer)
        
        return json.dumps({
            "is_correct": attempt.is_correct,
            "correct_answer": question.correct_answer,
            "error_type": attempt.error_type,
            "explanation": question.explanation
        })
    finally:
        db.close()

@mcp.tool()
def update_mastery(student_id: int, concept_id: int, result: bool) -> str:
    """Manually apply mastery logs directly for a concept based on pass/fail outcomes."""
    db = SessionLocal()
    try:
        mastery = db.query(Mastery).filter(
            Mastery.student_id == student_id,
            Mastery.concept_id == concept_id
        ).first()
        
        score = 100.0 if result else 0.0
        
        if not mastery:
            mastery = Mastery(
                student_id=student_id,
                concept_id=concept_id,
                mastery_score=score,
                questions_attempted=1,
                questions_correct=1 if result else 0,
                confidence=0.0,
                last_attempt=datetime.now(timezone.utc)
            )
            db.add(mastery)
        else:
            mastery.questions_attempted += 1
            if result:
                mastery.questions_correct += 1
            mastery.mastery_score = (mastery.mastery_score * 0.7) + (score * 0.3)
            mastery.last_attempt = datetime.now(timezone.utc)
            
        db.commit()
        db.refresh(mastery)
        return json.dumps({
            "student_id": student_id,
            "concept_id": concept_id,
            "mastery_score": mastery.mastery_score,
            "questions_attempted": mastery.questions_attempted,
            "questions_correct": mastery.questions_correct
        })
    finally:
        db.close()

@mcp.tool()
def recommend_next_topic(student_id: int) -> str:
    """Get the recommended next math concept for the student to study."""
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return f"Error: Student with ID {student_id} not found."
            
        concept = AdaptiveEngineService.recommend_next_concept(db, student_id, student.class_level)
        if not concept:
            return json.dumps({"recommended_concept": None})
            
        return json.dumps({
            "id": concept.id,
            "name": concept.name,
            "class_level": concept.class_level,
            "difficulty": concept.difficulty
        })
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    # Allow stdio running
    mcp.run()
