from .ollama import generate_response


def generate_report(student, role, score, total):

    prompt = f"""
You are an expert AI Career Counselor.

Student Details:

Name: {student.full_name}
Education: {student.education}
Branch: {student.branch}
Skills: {student.skills}
Interests: {student.interests}

Selected Job Role:
{role}

Aptitude Test Score:
{score}/{total}

Generate a detailed report with these headings:

1. Career Suitability
2. Strengths
3. Weaknesses
4. Skills to Improve
5. Recommended Certifications
6. Project Ideas
7. Salary Range
8. Learning Roadmap
9. Final Recommendation
"""

    return generate_response(prompt)