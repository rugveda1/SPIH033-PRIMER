from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AssessmentStartIn(BaseModel):
    assessment_type: str  # 'diagnostic', 'topic', 'revision'
    concept_id: Optional[int] = None

class AssessmentQuestionResponse(BaseModel):
    id: int
    question_text: str
    options: List[str]

class AssessmentStartOut(BaseModel):
    assessment_id: int
    assessment_type: str
    questions: List[AssessmentQuestionResponse]

class AssessmentSubmitItem(BaseModel):
    question_id: int
    submitted_answer: str

class AssessmentSubmitIn(BaseModel):
    answers: List[AssessmentSubmitItem]

class AssessmentQuestionResult(BaseModel):
    question_id: int
    question_text: str
    submitted_answer: str
    correct_answer: str
    is_correct: bool
    explanation: Optional[str] = None

class AssessmentSubmitOut(BaseModel):
    assessment_id: int
    score: float
    results: List[AssessmentQuestionResult]
