from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tutor_auth.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    # Setup test DB tables
    Base.metadata.create_all(bind=engine)
    
    # Override get_db dependency
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
        
    # Teardown test DB tables
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)

def test_signup(client):
    response = client.post("/api/auth/signup", json={
        "name": "Jane Doe",
        "email": "jane@example.com",
        "password": "testpassword123",
        "class_level": 2
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["email"] == "jane@example.com"
    assert data["class_level"] == 2
    assert "id" in data

def test_signup_duplicate_email(client):
    response = client.post("/api/auth/signup", json={
        "name": "Another Name",
        "email": "jane@example.com",
        "password": "anotherpassword",
        "class_level": 1
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_json(client):
    response = client.post("/api/auth/login-json", json={
        "email": "jane@example.com",
        "password": "testpassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_form(client):
    response = client.post("/api/auth/login", data={
        "username": "jane@example.com",
        "password": "testpassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_login_incorrect_password(client):
    response = client.post("/api/auth/login-json", json={
        "email": "jane@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_get_current_student_unauthenticated(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401

def test_get_current_student_authenticated(client):
    login_response = client.post("/api/auth/login-json", json={
        "email": "jane@example.com",
        "password": "testpassword123"
    })
    token = login_response.json()["access_token"]
    
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "jane@example.com"
