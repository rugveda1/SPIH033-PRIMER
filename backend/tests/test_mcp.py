import pytest
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import backend.database as database_module
import backend.mcp_server as mcp_server_module
from backend.database import Base
from backend.data.seed import seed_data
from backend.models.student import Student
from backend.mcp_server import (
    get_student_profile,
    get_concept,
    get_prerequisites,
    get_mastery,
    get_weak_topics,
    get_learning_context,
    generate_question,
    evaluate_answer,
    update_mastery,
    recommend_next_topic
)

TEST_DATABASE_URL = "sqlite:///./test_tutor_mcp.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="module", autouse=True)
def setup_mcp_test_db():
    database_module.SessionLocal = TestingSessionLocal
    mcp_server_module.SessionLocal = TestingSessionLocal
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        # Seed mathematical concepts
        seed_data(db)
        # Create a test student
        student = Student(id=1, name="MCP Tester", email="mcp@test.com", password_hash="hash", class_level=1)
        db.add(student)
        db.commit()
    finally:
        db.close()
        
    yield
    Base.metadata.drop_all(bind=test_engine)

def test_mcp_tools():
    # 1. get_student_profile
    profile = get_student_profile(1)
    assert "MCP Tester" in profile
    assert "mcp@test.com" in profile

    # 2. get_concept
    concept = get_concept(1)
    assert "Counting" in concept

    # 3. get_prerequisites
    prereqs = get_prerequisites(12)
    data = json.loads(prereqs)
    assert 4 in data["direct_prerequisites"]

    # 4. get_mastery
    mastery = get_mastery(1, 1)
    assert "mastery_score" in mastery

    # 5. get_weak_topics
    weak = get_weak_topics(1)
    assert "Counting" in weak

    # 6. get_learning_context
    context = get_learning_context(1, 12)
    assert "prerequisite_mastery" in context

    # 7. generate_question
    q = generate_question(1, "easy", "mcq")
    assert "question_text" in q

    # 8. evaluate_answer
    ans = evaluate_answer(1, "3", student_id=1)
    assert "is_correct" in ans

    # 9. update_mastery
    update = update_mastery(1, 1, True)
    assert "mastery_score" in update

    # 10. recommend_next_topic
    rec = recommend_next_topic(1)
    assert "Counting" in rec or "Numbers" in rec
