import requests


def generate_response(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def get_career_recommendation(student, score):

    prompt = f"""
You are an expert AI Career Counselor.

Student Details:

Name: {student.full_name}
Education: {student.education}
Branch: {student.branch}
Skills: {student.skills}
Interests: {student.interests}

Aptitude Test Score:
{score}

Based on the above information provide:

1. Best Career
2. Why this career?
3. Skills to Improve
4. 6-Month Learning Roadmap
5. Expected Salary in India
6. Overall Confidence Score (0-100%)
"""

    return generate_response(prompt)