"""Role suggestions used before a student confirms their assessment scope."""
import json
import requests


FALLBACK_ROLES = [
    ("Software Engineer", "Builds and maintains reliable software products."),
    ("Data Analyst", "Turns data into clear business insights and decisions."),
    ("Cloud Engineer", "Designs and operates scalable cloud infrastructure."),
    ("QA Engineer", "Improves product quality through testing and automation."),
    ("Product Designer", "Uses research and interface design to solve user problems."),
]


def recommend_roles(interests, current_roles):
    """Return safe, concise AI suggestions; keep the UI usable if Ollama is down."""
    selected = {role.casefold() for role in current_roles}
    prompt = f"""
You are a career adviser. Suggest 3 to 5 complementary job roles for a student.
Interests: {interests or 'Not provided'}
Current target roles: {', '.join(current_roles) or 'None'}
Return JSON only: {{"roles": [{{"name": "Role", "reason": "Short specific reason"}}]}}.
Do not repeat current roles. Keep every reason under 24 words.
"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2:3b", "prompt": prompt, "stream": False, "format": "json"},
            timeout=45,
        )
        response.raise_for_status()
        items = json.loads(response.json()["response"]).get("roles", [])
        roles = [
            {"name": item["name"].strip(), "reason": item["reason"].strip()}
            for item in items
            if isinstance(item, dict) and item.get("name") and item.get("reason")
            and item["name"].casefold() not in selected
        ]
        if roles:
            return {"roles": roles[:5]}
    except (requests.RequestException, ValueError, KeyError, TypeError):
        pass

    return {"roles": [
        {"name": name, "reason": reason}
        for name, reason in FALLBACK_ROLES if name.casefold() not in selected
    ][:5]}
