from backend.api.auth import router as auth_router
from backend.api.concepts import router as concepts_router
from backend.api.practice import router as practice_router
from backend.api.assessments import router as assessments_router
from backend.api.chat import router as chat_router
from backend.api.recommendations import router as recommendations_router

__all__ = [
    "auth_router",
    "concepts_router",
    "practice_router",
    "assessments_router",
    "chat_router",
    "recommendations_router",
]
