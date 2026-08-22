import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models.student import Student
from backend.models.concept import Concept, ConceptRelationship
from backend.models.question import Question

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tutor.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_db_setup(db_session):
    # Verify table creation and base queries
    students_count = db_session.query(Student).count()
    assert students_count == 0

def test_create_and_query_entities(db_session):
    # Create concept
    concept = Concept(
        id=999,
        name="Test Concept",
        description="Verify database schemas",
        class_level=1,
        difficulty="easy",
        learning_objectives=["objective 1"]
    )
    db_session.add(concept)
    db_session.commit()

    queried_concept = db_session.query(Concept).filter(Concept.id == 999).first()
    assert queried_concept is not None
    assert queried_concept.name == "Test Concept"
    assert "objective 1" in queried_concept.learning_objectives

    # Create question mapped to concept
    question = Question(
        concept_id=999,
        class_level=1,
        difficulty="easy",
        question_type="mcq",
        question_text="What is 1+1?",
        options=["1", "2", "3"],
        correct_answer="2",
        explanation="Simple addition"
    )
    db_session.add(question)
    db_session.commit()

    queried_q = db_session.query(Question).filter(Question.concept_id == 999).first()
    assert queried_q is not None
    assert queried_q.question_text == "What is 1+1?"
