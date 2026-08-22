import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models.student import Student
from backend.models.concept import Concept, ConceptRelationship
from backend.models.mastery import Mastery
from backend.services.adaptive_engine import AdaptiveEngineService

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tutor_adaptive_service.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    
    c1 = Concept(id=1, name="Concept 1", description="C1 desc", class_level=1, difficulty="easy")
    c2 = Concept(id=2, name="Concept 2", description="C2 desc", class_level=1, difficulty="medium")
    c3 = Concept(id=3, name="Concept 3", description="C3 desc", class_level=1, difficulty="hard")
    
    rel = ConceptRelationship(source_concept_id=1, target_concept_id=2, relationship_type="prerequisite_for")
    student = Student(id=1, name="Charlie Test", email="charlie@test.com", password_hash="hash", class_level=1)
    
    session.add_all([c1, c2, c3, rel, student])
    session.commit()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_recommendation_locked_prereq(db_session):
    rec = AdaptiveEngineService.recommend_next_concept(db_session, student_id=1, class_level=1)
    assert rec is not None
    assert rec.id == 1

def test_recommendation_unlocked_prereq(db_session):
    m1 = Mastery(student_id=1, concept_id=1, mastery_score=85.0)
    db_session.add(m1)
    db_session.commit()

    rec = AdaptiveEngineService.recommend_next_concept(db_session, student_id=1, class_level=1)
    assert rec is not None
    assert rec.id == 2

def test_recommendation_review_all_mastered(db_session):
    m2 = Mastery(student_id=1, concept_id=2, mastery_score=90.0)
    m3 = Mastery(student_id=1, concept_id=3, mastery_score=80.0)
    db_session.add_all([m2, m3])
    db_session.commit()

    # C3 has the lowest score (80%) and should be selected for review
    rec = AdaptiveEngineService.recommend_next_concept(db_session, student_id=1, class_level=1)
    assert rec is not None
    assert rec.id == 3
