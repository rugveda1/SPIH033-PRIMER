from pydantic import BaseModel
from typing import List, Optional

class PracticeQuestionOut(BaseModel):
    id: int
    concept_id: int
    class_level: int
    difficulty: str
    question_type: str
    question_text: str
    options: List[str]

    model_config = {
        "from_attributes": True
    }

class PracticeSubmitIn(BaseModel):
    question_id: int
    submitted_answer: str

class PracticeSubmitOut(BaseModel):
    attempt_id: int
    is_correct: bool
    correct_answer: str
    error_type: str
    explanation: Optional[str] = None
