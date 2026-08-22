from typing import List, Set, Dict
from sqlalchemy.orm import Session
from backend.models.concept import Concept, ConceptRelationship
from backend.models.mastery import Mastery
from backend.schemas.concept import ConceptOut, PrerequisiteStatus, ConceptReadiness

class KnowledgeGraphService:
    @staticmethod
    def get_direct_prerequisites(db: Session, concept_id: int) -> List[Concept]:
        """
        Fetch direct prerequisite concepts for a given concept.
        """
        relationships = db.query(ConceptRelationship).filter(
            ConceptRelationship.target_concept_id == concept_id,
            ConceptRelationship.relationship_type == "prerequisite_for"
        ).all()
        return [rel.source_concept for rel in relationships]

    @classmethod
    def get_recursive_prerequisites(cls, db: Session, concept_id: int) -> Set[int]:
        """
        Recursively fetch all descendant concept IDs that are prerequisites (directly or transitively)
        for the given target concept.
        """
        prereqs: Set[int] = set()
        visited: Set[int] = set()
        to_visit = [concept_id]

        while to_visit:
            current_id = to_visit.pop(0)
            if current_id in visited:
                continue
            visited.add(current_id)

            relationships = db.query(ConceptRelationship).filter(
                ConceptRelationship.target_concept_id == current_id,
                ConceptRelationship.relationship_type == "prerequisite_for"
            ).all()

            for rel in relationships:
                prereqs.add(rel.source_concept_id)
                to_visit.append(rel.source_concept_id)

        return prereqs

    @classmethod
    def get_student_readiness(cls, db: Session, student_id: int, concept_id: int, threshold: float = 80.0) -> ConceptReadiness:
        """
        Evaluate if a student is ready to study a concept.
        Ready means all direct prerequisites are mastered (mastery_score >= threshold).
        """
        concept = db.query(Concept).filter(Concept.id == concept_id).first()
        if not concept:
            raise ValueError(f"Concept with ID {concept_id} not found")

        direct_prereqs = cls.get_direct_prerequisites(db, concept_id)
        
        prereq_statuses = []
        is_ready = True

        for p in direct_prereqs:
            mastery = db.query(Mastery).filter(
                Mastery.student_id == student_id,
                Mastery.concept_id == p.id
            ).first()

            score = mastery.mastery_score if mastery else 0.0
            is_mastered = score >= threshold
            
            if not is_mastered:
                is_ready = False

            prereq_statuses.append(
                PrerequisiteStatus(
                    concept=ConceptOut.model_validate(p),
                    mastery_score=score,
                    is_mastered=is_mastered
                )
            )

        return ConceptReadiness(
            concept=ConceptOut.model_validate(concept),
            is_ready=is_ready,
            prerequisites=prereq_statuses
        )
