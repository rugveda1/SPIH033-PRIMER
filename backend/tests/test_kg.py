from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.main import app
from backend.models.mastery import Mastery
from backend.models.student import Student

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tutor_kg.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    # Setup test DB tables (this also triggers the autoseed logic in main.py)
    Base.metadata.create_all(bind=engine)
    
    # Seed the test database explicitly
    db = TestingSessionLocal()
    try:
        from backend.data.seed import seed_data
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

def test_auto_seed_concepts(client):
    response = client.get("/api/concepts")
    assert response.status_code == 200
    concepts = response.json()
    assert len(concepts) > 0
    assert any(c["id"] == 1 and c["name"] == "Counting" for c in concepts)

def test_get_concepts_by_class_level(client):
    response = client.get("/api/concepts?class_level=1")
    assert response.status_code == 200
    concepts = response.json()
    assert len(concepts) > 0
    assert all(c["class_level"] == 1 for c in concepts)
    
    response = client.get("/api/concepts?class_level=5")
    assert response.status_code == 200
    concepts = response.json()
    assert len(concepts) > 0
    assert all(c["class_level"] == 5 for c in concepts)

def test_prerequisites_direct_and_recursive(client):
    # Two-Digit Addition (ID 12) has direct prerequisites Addition Intro (ID 4) and Place Value to 1000 (ID 11)
    response = client.get("/api/concepts/12/prerequisites")
    assert response.status_code == 200
    direct = response.json()
    direct_ids = [d["id"] for d in direct]
    assert 4 in direct_ids
    assert 11 in direct_ids
    
    # Recursive prerequisites for Two-Digit Addition (ID 12)
    response = client.get("/api/concepts/12/prerequisites?recursive=true")
    assert response.status_code == 200
    recursive = response.json()
    recursive_ids = [r["id"] for r in recursive]
    assert 1 in recursive_ids  # Counting
    assert 2 in recursive_ids  # Numbers 1-100
    assert 3 in recursive_ids  # Place Value Intro
    assert 4 in recursive_ids  # Addition Intro
    assert 10 in recursive_ids  # Numbers up to 1000
    assert 11 in recursive_ids  # Place Value to 1000

def test_student_readiness_checks(client):
    signup_response = client.post("/api/auth/signup", json={
        "name": "Math Whiz",
        "email": "whiz@example.com",
        "password": "passphrase123",
        "class_level": 2
    })
    assert signup_response.status_code == 201
    
    login_response = client.post("/api/auth/login-json", json={
        "email": "whiz@example.com",
        "password": "passphrase123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Check readiness for concept 1 (Counting) - has no prerequisites, should be ready (True)
    response = client.get("/api/concepts/1/ready", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["concept"]["id"] == 1
    assert data["is_ready"] is True
    assert len(data["prerequisites"]) == 0
    
    # Check readiness for concept 12 (Two-Digit Addition) - student has no mastery yet, should be not ready (False)
    response = client.get("/api/concepts/12/ready", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["concept"]["id"] == 12
    assert data["is_ready"] is False
    assert len(data["prerequisites"]) == 2
    
    # Manually seed mastery for concept 4 and concept 11
    db = TestingSessionLocal()
    student = db.query(Student).filter(Student.email == "whiz@example.com").first()
    
    mastery_4 = Mastery(student_id=student.id, concept_id=4, mastery_score=85.0)
    mastery_11 = Mastery(student_id=student.id, concept_id=11, mastery_score=90.0)
    db.add_all([mastery_4, mastery_11])
    db.commit()
    db.close()
    
    # Re-check readiness, now it should be ready (True)
    response = client.get("/api/concepts/12/ready", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["is_ready"] is True
    
    statuses = {p["concept"]["id"]: p for p in data["prerequisites"]}
    assert statuses[4]["mastery_score"] == 85.0
    assert statuses[4]["is_mastered"] is True
    assert statuses[11]["mastery_score"] == 90.0
    assert statuses[11]["is_mastered"] is True
