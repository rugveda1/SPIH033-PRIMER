from typing import List, Optional
from pydantic import BaseModel

class ConceptOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    class_level: int
    difficulty: str
    learning_objectives: List[str] = []

    model_config = {
        "from_attributes": True
    }

class ConceptRelationshipOut(BaseModel):
    id: int
    source_concept_id: int
    target_concept_id: int
    relationship_type: str

    model_config = {
        "from_attributes": True
    }

class PrerequisiteStatus(BaseModel):
    concept: ConceptOut
    mastery_score: float
    is_mastered: bool

class ConceptReadiness(BaseModel):
    concept: ConceptOut
    is_ready: bool
    prerequisites: List[PrerequisiteStatus]
