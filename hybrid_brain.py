
import os
import openai
from dotenv import load_dotenv

# Load your OpenAI API key securely from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def smith_brain(task):
    """
    Hybrid Brain Logic:
    - If the task is a known command, respond with offline logic.
    - If not, fallback to GPT for intelligent reply.
    """
    # Offline logic mapping
    offline_responses = {
        "activate mission": "Mission activated. SmithCore is now live.",
        "generate report": "System diagnostic report ready. All systems normal.",
        "status update": "All core modules are stable. No anomalies detected.",
        "launch content engine": "AIMomentum Content System launched. Awaiting inputs."
    }

    for command in offline_responses:
        if command in task.lower():
            return offline_responses[command]

    # Fallback to GPT if no offline command matched
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are SmithCore, an AI execution engine, assisting with tasks and decisions."},
                {"role": "user", "content": task}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"[GPT fallback failed: {e}]"
