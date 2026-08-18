import json
import requests


def generate_roles(student, category):

    prompt = f"""
You are an expert AI Career Guidance Assistant.

Analyze the student's profile and suggest the TOP 10 most suitable and in-demand job roles.

Student Details:

Education:
{student.education}

Branch:
{student.branch}

Year:
{student.year}

Skills:
{student.skills}

Interests:
{student.interests}

Selected Career Category:
{category}

Instructions:

- Suggest exactly 10 job roles.
- Include both entry-level and advanced careers.
- Roles must match the student's education, branch, skills, interests and selected category.
- Each role should have a short description (1-2 sentences).
- Return ONLY valid JSON.
- Do not use markdown.
- Do not add explanations.

Return this format exactly:

{{
    "roles": [
        {{
            "name": "AI Engineer",
            "description": "Develops intelligent AI applications using machine learning."
        }},
        {{
            "name": "Machine Learning Engineer",
            "description": "Builds predictive models using AI algorithms."
        }}
    ]
}}
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

        print("\n========== AI ROLE RESPONSE ==========\n")
        print(result)
        print("\n======================================\n")

        return {
            "roles": []
        }