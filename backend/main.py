from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import Base, engine, SessionLocal
from backend.api import (
    auth_router,
    concepts_router,
    practice_router,
    assessments_router,
    chat_router,
    recommendations_router,
)
from backend.data.seed import seed_data
from backend.models.concept import Concept

# Ensure database tables are created at startup
Base.metadata.create_all(bind=engine)

# Auto-seed if database is empty
db = SessionLocal()
try:
    if db.query(Concept).count() == 0:
        print("Database concepts are empty. Running auto-seed...")
        seed_data(db)
        print("Auto-seed successful!")
except Exception as e:
    print(f"Failed to auto-seed database: {e}")
finally:
    db.close()

app = FastAPI(
    title="Adaptive AI Mathematics Tutor API",
    description="FastAPI Backend for Adaptive Math Tutoring (Classes 1-5)",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register endpoints
app.include_router(auth_router)
app.include_router(concepts_router)
app.include_router(practice_router)
app.include_router(assessments_router)
app.include_router(chat_router)
app.include_router(recommendations_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Adaptive AI Math Tutor API",
        "documentation": "/docs"
    }
