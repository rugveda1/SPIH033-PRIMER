from sqlalchemy.orm import Session
from backend.models.concept import Concept
from backend.models.mastery import Mastery
from backend.services.knowledge_graph import KnowledgeGraphService

class AdaptiveEngineService:
    @staticmethod
    def recommend_next_concept(db: Session, student_id: int, class_level: int) -> Concept:
        """
        Determines the recommended next concept to study based on class level,
        mastery scores, and prerequisite readiness.
        """
        concepts = db.query(Concept).filter(Concept.class_level == class_level).order_by(Concept.id).all()
        if not concepts:
            return None

        # Map current student mastery
        mastery_records = db.query(Mastery).filter(Mastery.student_id == student_id).all()
        mastery_map = {m.concept_id: m.mastery_score for m in mastery_records}

        unmastered_concepts = []

        for concept in concepts:
            score = mastery_map.get(concept.id, 0.0)
            is_mastered = score >= 80.0
            
            if not is_mastered:
                unmastered_concepts.append(concept)
                readiness = KnowledgeGraphService.get_student_readiness(db, student_id, concept.id)
                if readiness.is_ready:
                    # Return the first unmastered concept that the student is ready to take
                    return concept

        # If all concepts are mastered, recommend the one with the lowest score for review
        if not unmastered_concepts:
            lowest_concept = None
            lowest_score = 101.0
            for concept in concepts:
                score = mastery_map.get(concept.id, 0.0)
                if score < lowest_score:
                    lowest_score = score
                    lowest_concept = concept
            return lowest_concept

        # Fallback to the first unmastered concept if they are all locked (should not happen with structured seeds)
        return unmastered_concepts[0]
