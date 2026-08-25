import requests


def generate_response(prompt):

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2:3b", "prompt": prompt, "stream": False},
            timeout=90,
        )
        response.raise_for_status()
        return response.json().get("response", "We could not generate a detailed AI summary.")
    except (requests.RequestException, ValueError, KeyError):
        return "AI summary is temporarily unavailable. Your personalised learning roadmap is still ready below."
