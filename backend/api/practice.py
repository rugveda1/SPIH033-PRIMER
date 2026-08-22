import random
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.concept import Concept
from backend.models.question import Question
from backend.models.student import Student
from backend.models.mastery import Mastery
from backend.schemas.practice import PracticeQuestionOut, PracticeSubmitIn, PracticeSubmitOut
from backend.services.auth import get_current_student
from backend.services.mastery import MasteryService
from backend.services.grok import call_grok_api
from backend.services.knowledge_graph import KnowledgeGraphService

router = APIRouter(prefix="/api/practice", tags=["Practice"])

def create_dynamic_fallback_question(concept_id: int, concept_name: str, class_level: int) -> dict:
    """
    Constructs a dynamic mock question in memory if no questions exist in the DB for the concept.
    """
    name_lower = concept_name.lower()
    
    if "counting" in name_lower:
        return {
            "id": 1000 + concept_id,
            "concept_id": concept_id,
            "class_level": class_level,
            "difficulty": "easy",
            "question_type": "mcq",
            "question_text": "Count the apples: 🍎🍎🍎🍎🍎. How many apples are there?",
            "options": ["4", "5", "6", "7"],
            "correct_answer": "5",
            "explanation": "If we count the apples one by one, we get exactly 5 apples!"
        }
    elif "value" in name_lower:
        return {
            "id": 1000 + concept_id,
            "concept_id": concept_id,
            "class_level": class_level,
            "difficulty": "medium",
            "question_type": "mcq",
            "question_text": "In the number 42, what is the value of the digit in the tens place?",
            "options": ["2", "4", "40", "20"],
            "correct_answer": "40",
            "explanation": "The 4 is in the tens place, so it represents 4 tens, which is 40."
        }
    elif "addition" in name_lower:
        num1 = random.randint(5, 15)
        num2 = random.randint(2, 9)
        ans = num1 + num2
        opts = list(set([ans, ans + 1, ans - 1, ans + 2]))
        random.shuffle(opts)
        return {
            "id": 1000 + concept_id,
            "concept_id": concept_id,
            "class_level": class_level,
            "difficulty": "easy",
            "question_type": "mcq",
            "question_text": f"What is {num1} + {num2}?",
            "options": [str(o) for o in opts],
            "correct_answer": str(ans),
            "explanation": f"Putting {num1} and {num2} together gives us {ans}."
        }
    elif "subtraction" in name_lower:
        num1 = random.randint(10, 20)
        num2 = random.randint(2, 9)
        ans = num1 - num2
        opts = list(set([ans, ans + 1, ans - 1, ans + 2]))
        random.shuffle(opts)
        return {
            "id": 1000 + concept_id,
            "concept_id": concept_id,
            "class_level": class_level,
            "difficulty": "easy",
            "question_type": "mcq",
            "question_text": f"What is {num1} - {num2}?",
            "options": [str(o) for o in opts],
            "correct_answer": str(ans),
            "explanation": f"Starting with {num1} and taking away {num2} leaves us with {ans}."
        }
    elif "multiplication" in name_lower:
        num1 = random.randint(3, 9)
        num2 = random.randint(2, 9)
        ans = num1 * num2
        opts = list(set([ans, ans + num1, ans - num2, ans + 2]))
        random.shuffle(opts)
        return {
            "id": 1000 + concept_id,
            "concept_id": concept_id,
            "class_level": class_level,
            "difficulty": "medium",
            "question_type": "mcq",
            "question_text": f"What is {num1} x {num2}?",
            "options": [str(o) for o in opts],
            "correct_answer": str(ans),
            "explanation": f"{num1} groups of {num2} is equal to {ans}."
        }
    elif "fraction" in name_lower:
        return {
            "id": 1000 + concept_id,
            "concept_id": concept_id,
            "class_level": class_level,
            "difficulty": "medium",
            "question_type": "mcq",
            "question_text": "If we divide a pizza into 4 equal slices and eat 1 slice, what fraction of the pizza is eaten?",
            "options": ["1/2", "1/4", "3/4", "1/3"],
            "correct_answer": "1/4",
            "explanation": "Eating 1 slice out of 4 equal slices represents the fraction 1/4."
        }
    else:
        return {
            "id": 1000 + concept_id,
            "concept_id": concept_id,
            "class_level": class_level,
            "difficulty": "easy",
            "question_type": "mcq",
            "question_text": "What is 10 + 4?",
            "options": ["12", "13", "14", "15"],
            "correct_answer": "14",
            "explanation": "10 + 4 is equal to 14."
        }

@router.get("/question", response_model=PracticeQuestionOut)
def get_practice_question(concept_id: int, db: Session = Depends(get_db)):
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Concept with ID {concept_id} not found"
        )

    questions = db.query(Question).filter(Question.concept_id == concept_id).all()
    if questions:
        return random.choice(questions)

    q_dict = create_dynamic_fallback_question(concept_id, concept.name, concept.class_level)
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
    return temp_q

@router.post("/submit", response_model=PracticeSubmitOut)
def submit_practice_answer(
    payload: PracticeSubmitIn,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    q_id = payload.question_id
    ans = payload.submitted_answer

    # Retrieve or dynamically build fallback question
    question = db.query(Question).filter(Question.id == q_id).first()
    if not question:
        concept_id = q_id - 1000
        concept = db.query(Concept).filter(Concept.id == concept_id).first()
        if not concept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {q_id} not found"
            )
        q_dict = create_dynamic_fallback_question(concept_id, concept.name, concept.class_level)
        question = Question(
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
        db.add(question)

    try:
        attempt = MasteryService.evaluate_and_update_mastery(db, current_student.id, question.id, ans)
        
        explanation = question.explanation
        if not attempt.is_correct:
            # Trigger custom Socratic explanation via Grok on incorrect answer
            mastery = db.query(Mastery).filter(
                Mastery.student_id == current_student.id,
                Mastery.concept_id == question.concept_id
            ).first()
            mastery_score = mastery.mastery_score if mastery else 0.0

            prereqs = KnowledgeGraphService.get_direct_prerequisites(db, question.concept_id)
            prereqs_str = ", ".join([p.name for p in prereqs]) if prereqs else "None"

            prompt_messages = [
                {
                    "role": "user",
                    "content": f"I was solving the question: '{question.question_text}'. I submitted the answer: '{ans}', but the correct answer is '{question.correct_answer}'. Can you explain why my answer is incorrect and help me understand how to solve it?"
                }
            ]

            grok_context = {
                "class_level": current_student.class_level,
                "concept_name": question.concept.name,
                "difficulty": question.difficulty,
                "mastery_score": mastery_score,
                "learning_objectives": question.concept.learning_objectives,
                "prerequisites": prereqs_str,
                "recent_mistakes": [attempt.error_type],
                "recommended_next_step": "Try working on prerequisite concepts."
            }

            explanation = call_grok_api(prompt_messages, grok_context, mode="explain")

        return PracticeSubmitOut(
            attempt_id=attempt.id,
            is_correct=attempt.is_correct,
            correct_answer=question.correct_answer,
            error_type=attempt.error_type,
            explanation=explanation
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
