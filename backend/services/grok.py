import httpx
import logging
from backend.config import settings

logger = logging.getLogger(__name__)

def build_system_prompt(context: dict) -> str:
    class_level = context.get("class_level", 1)
    concept_name = context.get("concept_name", "Mathematics")
    difficulty = context.get("difficulty", "medium")
    mastery_score = context.get("mastery_score", 0.0)
    learning_objectives = context.get("learning_objectives", [])
    prerequisites = context.get("prerequisites", "None")
    recent_mistakes = context.get("recent_mistakes", [])
    recommended_next_step = context.get("recommended_next_step", "Keep practicing!")

    objectives_str = ", ".join(learning_objectives) if learning_objectives else "General math skills"
    mistakes_str = ", ".join(recent_mistakes) if recent_mistakes else "None"

    return f"""You are an Adaptive Socratic AI Mathematics Tutor for kids in Classes 1–5.
Your role is to guide the student to understand math concepts through friendly, supportive conversation.
Speak directly to the child. Use age-appropriate language (for Class {class_level}, approx {class_level + 5} years old), simple steps, concrete examples (e.g., apples, toys, cupcakes), and minimal technical jargon.
Never shame or discourage the child. Always maintain a highly supportive and warm tone.
IMPORTANT: Do not just give the final answer. Act Socratically by providing clues, hints, or guiding questions that help them discover the answer themselves.

Current Student Context:
- Class Level: Class {class_level}
- Concept: {concept_name} (Difficulty: {difficulty})
- Mastery Level: {mastery_score:.1f}/100
- Learning Objectives: {objectives_str}
- Prerequisites & Mastery: {prerequisites}
- Recent Mistakes/Patterns: {mistakes_str}
- Recommended Next Step: {recommended_next_step}

Guidelines:
1. Keep your responses short and punchy so a child does not get overwhelmed by text.
2. If they ask for a 'hint', give them a clear, bite-sized clue based on the current concept.
3. If they ask for an 'explanation', break the concept down step-by-step using concrete real-world objects.
4. If they made a calculation or place value mistake, gently explain what might have gone wrong without telling them the answer.
"""

def generate_fallback_response(user_message: str, context: dict, mode: str = "chat") -> str:
    concept = context.get("concept_name", "math")
    class_level = context.get("class_level", 1)
    
    if mode == "hint":
        return f"Clue: Let's look at {concept}! Since we are in Class {class_level}, try drawing it out or counting on your fingers. What do you get if you take it one step at a time? You can do this! 🌟"
    elif mode == "explain":
        return f"Let's break down {concept}! 🍎 Imagine you have objects in front of you. For Class {class_level}, we can think of it like grouping things together. If you have any questions, just tell me what part feels tricky!"
    else:
        # Conversational Chat mode fallback
        user_lower = user_message.lower()
        if "hint" in user_lower:
            return f"Here is a small hint for {concept}: Think about the steps we took in class. Try breaking the numbers down into tens and ones. What do you think comes next? 😊"
        elif "explain" in user_lower or "why" in user_lower or "how" in user_lower:
            return f"I'd love to explain {concept}! 🚀 For Class {class_level}, it's all about counting and finding patterns. Let's look at an example: if you have 3 apples and get 2 more, that makes 5! Can you try a similar one?"
        else:
            return f"Hi there! I am your Socratic Math Tutor. Let's explore {concept} together! 🎈 What would you like to practice or learn about next?"

def call_grok_api(messages: list, context: dict, mode: str = "chat") -> str:
    system_content = build_system_prompt(context)
    
    api_messages = [{"role": "system", "content": system_content}]
    for msg in messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})
        
    grok_key = settings.GROK_API_KEY
    if not grok_key or grok_key == "mock_key" or grok_key.startswith("your_"):
        last_user_msg = messages[-1]["content"] if messages else ""
        return generate_fallback_response(last_user_msg, context, mode)
        
    is_groq = grok_key.startswith("gsk_")
    api_url = "https://api.groq.com/openai/v1/chat/completions" if is_groq else "https://api.x.ai/v1/chat/completions"
    model_name = "llama-3.1-8b-instant" if is_groq else "grok-2"
        
    try:
        headers = {
            "Authorization": f"Bearer {grok_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model_name,
            "messages": api_messages,
            "temperature": 0.4,
            "max_tokens": 512
        }
        
        with httpx.Client() as client:
            response = client.post(api_url, headers=headers, json=data, timeout=10.0)
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                logger.warning(f"AI API returned status {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Error calling AI API: {e}")
        
    last_user_msg = messages[-1]["content"] if messages else ""
    return generate_fallback_response(last_user_msg, context, mode)
