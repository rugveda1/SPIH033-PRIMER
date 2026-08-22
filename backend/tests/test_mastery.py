import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models.student import Student
from backend.models.concept import Concept
from backend.models.question import Question
from backend.models.mastery import Mastery
from backend.models.attempt import Attempt
from backend.services.mastery import MasteryService

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tutor_mastery_service.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    
    student = Student(id=1, name="Bob Test", email="bob@test.com", password_hash="hash", class_level=1)
    concept = Concept(id=1, name="Counting", description="Counting", class_level=1, difficulty="easy")
    question = Question(id=1, concept_id=1, class_level=1, difficulty="easy", question_type="mcq", question_text="What is 1+1?", options=["1","2","3"], correct_answer="2", explanation="1+1=2")
    session.add_all([student, concept, question])
    session.commit()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_classify_error():
    err1 = MasteryService.classify_error("Two-Digit Addition", "42", "420")
    assert err1 == "place_value_error"

    err2 = MasteryService.classify_error("Counting", "5", "6")
    assert err2 == "calculation_error"

    err3 = MasteryService.classify_error("Multiplication Mastery", "56", "15")
    assert err3 == "multiplication_error"

def test_evaluate_and_update_mastery_correct(db_session):
    attempt = MasteryService.evaluate_and_update_mastery(db_session, student_id=1, question_id=1, submitted_answer="2")
    assert attempt.is_correct is True
    assert attempt.score == 100.0

    mastery = db_session.query(Mastery).filter(Mastery.student_id == 1, Mastery.concept_id == 1).first()
    assert mastery is not None
    assert mastery.questions_attempted == 1
    assert mastery.questions_correct == 1
    assert mastery.mastery_score == 100.0

def test_evaluate_and_update_mastery_incorrect(db_session):
    attempt = MasteryService.evaluate_and_update_mastery(db_session, student_id=1, question_id=1, submitted_answer="3")
    assert attempt.is_correct is False
    assert attempt.score == 0.0

    mastery = db_session.query(Mastery).filter(Mastery.student_id == 1, Mastery.concept_id == 1).first()
    assert mastery.questions_attempted == 2
    assert mastery.questions_correct == 1
    # EMA check: 100 * 0.7 + 0 * 0.3 = 70.0
    assert mastery.mastery_score == 70.0
