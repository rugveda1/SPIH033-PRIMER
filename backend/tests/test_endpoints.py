from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.main import app
from backend.data.seed import seed_data

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tutor_endpoints.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    # Setup test DB tables
    Base.metadata.create_all(bind=engine)
    
    # Seed the test database explicitly
    db = TestingSessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
        
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)

def test_endpoints_workflow(client):
    # 1. Signup and Login
    signup_res = client.post("/api/auth/signup", json={
        "name": "Endpoint Tester",
        "email": "endpoints@test.com",
        "password": "mypassword123",
        "class_level": 1
    })
    assert signup_res.status_code == 201
    
    login_res = client.post("/api/auth/login-json", json={
        "email": "endpoints@test.com",
        "password": "mypassword123"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. GET progress (baseline)
    prog_res = client.get("/api/auth/me/progress", headers=headers)
    assert prog_res.status_code == 200
    prog_data = prog_res.json()
    assert prog_data["overall_mastery"] == 0.0
    assert len(prog_data["completed_assessments"]) == 0
    
    # 3. GET recommendation
    rec_res = client.get("/api/recommendations/next", headers=headers)
    assert rec_res.status_code == 200
    rec_concept = rec_res.json()
    assert rec_concept["id"] == 1
    
    # 4. GET practice question for Counting (ID 1)
    q_res = client.get("/api/practice/question?concept_id=1", headers=headers)
    assert q_res.status_code == 200
    question = q_res.json()
    assert "question_text" in question
    
    # 5. POST practice submit (correct answer)
    ans_res = client.post("/api/practice/submit", headers=headers, json={
        "question_id": question["id"],
        "submitted_answer": "3"  # Mock counting correct choice
    })
    assert ans_res.status_code == 200
    
    # 6. POST chat message
    chat_res = client.post("/api/chat", headers=headers, json={
        "message": "Hi, tutor!",
        "concept_id": 1
    })
    assert chat_res.status_code == 200
    assert chat_res.json()["role"] == "assistant"
    
    # 7. POST chat hint
    hint_res = client.post("/api/chat/hint", headers=headers, json={
        "concept_id": 1,
        "question_id": question["id"]
    })
    assert hint_res.status_code == 200
    assert "hint" in hint_res.json()

    # 8. POST chat explain
    exp_res = client.post("/api/chat/explain", headers=headers, json={
        "concept_id": 1
    })
    assert exp_res.status_code == 200
    assert "explanation" in exp_res.json()
    
    # 9. POST start assessment
    ass_res = client.post("/api/assessments/start", headers=headers, json={
        "assessment_type": "diagnostic"
    })
    assert ass_res.status_code == 200
    ass_data = ass_res.json()
    assert len(ass_data["questions"]) == 5
    
    # 10. POST submit assessment answers
    submit_payload = {
        "answers": [{"question_id": q["id"], "submitted_answer": "3"} for q in ass_data["questions"]]
    }
    submit_res = client.post(f"/api/assessments/{ass_data['assessment_id']}/submit", headers=headers, json=submit_payload)
    assert submit_res.status_code == 200
    assert "score" in submit_res.json()
