import pytest
from backend.services.grok import call_grok_api, build_system_prompt, generate_fallback_response

def test_build_system_prompt():
    context = {
        "class_level": 2,
        "concept_name": "Two-Digit Addition",
        "difficulty": "medium",
        "mastery_score": 45.0,
        "learning_objectives": ["Add with regrouping"],
        "prerequisites": "Addition Intro (Mastered, 90%)",
        "recent_mistakes": ["calculation_error"],
        "recommended_next_step": "Practice regrouping"
    }
    prompt = build_system_prompt(context)
    assert "Class 2" in prompt
    assert "Two-Digit Addition" in prompt
    assert "45.0" in prompt
    assert "Add with regrouping" in prompt

def test_generate_fallback_response():
    context = {"concept_name": "Counting", "class_level": 1}
    res_hint = generate_fallback_response("give me a hint", context, mode="hint")
    assert "Clue" in res_hint
    assert "Counting" in res_hint

    res_explain = generate_fallback_response("explain", context, mode="explain")
    assert "break down" in res_explain
    assert "Counting" in res_explain

def test_call_grok_api_fallback():
    context = {"concept_name": "Counting", "class_level": 1}
    messages = [{"role": "user", "content": "I need help with Counting"}]
    res = call_grok_api(messages, context, mode="chat")
    assert "Socratic" in res or "Counting" in res
