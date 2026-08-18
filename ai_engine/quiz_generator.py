import json
import requests


def generate_quiz(student, role):

    prompt = f"""
You are an expert Aptitude Test Generator.

Generate exactly 10 multiple-choice aptitude questions for the role:

{role}

Student Profile:
Education: {student.education}
Branch: {student.branch}
Skills: {student.skills}
Interests: {student.interests}

Return ONLY valid JSON.

Format:

{{
    "questions":[
        {{
            "question":"Question here",
            "options":[
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer":"Correct Option"
        }}
    ]
}}

Rules:

- Exactly 10 questions.
- Exactly 4 options.
- Answer must exactly match one option.
- Do NOT use markdown.
- Do NOT explain anything.
- Return JSON only.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False,
            "format": "json"
        },
        timeout=180
    )

    result = response.json()["response"].strip()

    print("\n========== QUIZ RESPONSE ==========\n")
    print(result)
    print("\n===================================\n")

    try:
        return json.loads(result)

    except json.JSONDecodeError as e:

        print("\nJSON ERROR:\n", e)

        raise