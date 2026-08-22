from datetime import datetime, timezone
import re
from sqlalchemy.orm import Session
from backend.models.attempt import Attempt
from backend.models.mastery import Mastery
from backend.models.question import Question
from backend.models.concept import Concept

class MasteryService:
    @staticmethod
    def classify_error(concept_name: str, correct_val: str, student_val: str) -> str:
        """
        Determines the type of error a student made based on mathematical heuristics.
        Returns: conceptual_error, calculation_error, place_value_error,
                 multiplication_error, division_error, careless_error, unknown
        """
        correct_clean = correct_val.strip().lower()
        student_clean = student_val.strip().lower()

        if correct_clean == student_clean:
            return "unknown"

        # Look for numbers in both answers
        correct_nums = re.findall(r"\d+", correct_clean)
        student_nums = re.findall(r"\d+", student_clean)

        if correct_nums and student_nums:
            try:
                c_num = int(correct_nums[0])
                s_num = int(student_nums[0])

                # Place Value Error: off by factor of 10 or 100
                if s_num == c_num * 10 or s_num == c_num * 100 or c_num == s_num * 10 or c_num == s_num * 100:
                    return "place_value_error"

                # Calculation Error: off by a small addition/subtraction slip (1 or 2)
                if abs(c_num - s_num) in [1, 2]:
                    return "calculation_error"

                # Operations specific errors
                concept_lower = concept_name.lower()
                if "multiplication" in concept_lower:
                    return "multiplication_error"
                elif "division" in concept_lower:
                    return "division_error"
                
                # Default numeric error classification
                return "calculation_error"
            except ValueError:
                pass

        return "conceptual_error"

    @classmethod
    def evaluate_and_update_mastery(
        cls, db: Session, student_id: int, question_id: int, submitted_answer: str
    ) -> Attempt:
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise ValueError(f"Question with ID {question_id} not found")

        # Deterministic comparison
        correct_answer = question.correct_answer.strip().lower()
        submitted_clean = submitted_answer.strip().lower()
        is_correct = correct_answer == submitted_clean
        score = 100.0 if is_correct else 0.0

        # Classify error
        error_type = "unknown"
        if not is_correct:
            error_type = cls.classify_error(question.concept.name, question.correct_answer, submitted_answer)

        # Create attempt log
        attempt = Attempt(
            student_id=student_id,
            question_id=question_id,
            submitted_answer=submitted_answer,
            is_correct=is_correct,
            score=score,
            error_type=error_type,
            created_at=datetime.now(timezone.utc)
        )
        db.add(attempt)

        # Retrieve or create mastery
        mastery = db.query(Mastery).filter(
            Mastery.student_id == student_id,
            Mastery.concept_id == question.concept_id
        ).first()

        if not mastery:
            mastery = Mastery(
                student_id=student_id,
                concept_id=question.concept_id,
                mastery_score=score,
                questions_attempted=1,
                questions_correct=1 if is_correct else 0,
                confidence=0.0,
                last_attempt=datetime.now(timezone.utc)
            )
            db.add(mastery)
        else:
            mastery.questions_attempted += 1
            if is_correct:
                mastery.questions_correct += 1
            
            # Update score with Exponential Moving Average (EMA)
            mastery.mastery_score = (mastery.mastery_score * 0.7) + (score * 0.3)
            mastery.last_attempt = datetime.now(timezone.utc)

        db.commit()
        db.refresh(attempt)
        return attempt
