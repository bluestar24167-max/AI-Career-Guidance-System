import json
import requests


def generate_categories(student):

    prompt = f"""
You are an expert AI Career Guidance Assistant.

Analyze the student's profile.

Student Details:

Education: {student.education}
Branch: {student.branch}
Year: {student.year}
Skills: {student.skills}
Interests: {student.interests}

IMPORTANT:

Suggest ONLY broad career categories.

DO NOT return job titles.

Examples of VALID categories:

- Artificial Intelligence
- Software Development
- Data Science
- Cyber Security
- Cloud Computing
- DevOps
- Mobile App Development
- Web Development
- UI/UX Design
- Digital Marketing
- Business Analytics
- Networking
- Robotics
- Game Development
- Embedded Systems

Examples of INVALID answers:

- AI Engineer
- UI/UX Designer
- Software Engineer
- Data Scientist
- Frontend Developer
- Backend Developer

Return ONLY valid JSON in this exact format:

{{
    "categories": [
        {{
            "name": "Artificial Intelligence",
            "description": "Careers involving machine learning and intelligent systems."
        }}
    ]
}}

Do not use markdown.
Do not explain.
Return JSON only.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False,
            "format": "json"
        },
        timeout=120
    )

    result = response.json()["response"].strip()

    try:
        return json.loads(result)

    except json.JSONDecodeError:
        print("\n====== AI CATEGORY RESPONSE ======\n")
        print(result)
        print("\n==================================\n")

        return {"categories": []}