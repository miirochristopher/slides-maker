import os
import requests

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_GENERATE_URL = f"{OLLAMA_BASE_URL}/api/generate"

def generate_slide_content(text: str):
    prompt = f"""
    Generate PowerPoint slide content.
    Return JSON ONLY with:
    - title
    - bullet_points (max 5)

    Topic:
    {text}
    """

    response = requests.post(
        OLLAMA_GENERATE_URL,
        json={
            "model": "llama3.3:3b",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    raw = response.json()["response"]

    import json
    return json.loads(raw)
