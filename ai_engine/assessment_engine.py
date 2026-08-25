"""Job-specific assessment and post-assessment analysis services."""
import json
import requests
from ai_engine.roadmap import build_learning_roadmap


def _fallback_questions(roles):
    role_text = ", ".join(roles)
    seed_questions = [
        {"question": f"Which step best helps validate requirements for a {role_text} task?", "options": ["Clarify success criteria and constraints", "Start implementation without context", "Skip stakeholder feedback", "Only copy an old solution"], "answer": "Clarify success criteria and constraints", "skill": "Problem solving"},
        {"question": "What is the most reliable way to make work reproducible?", "options": ["Document assumptions and version changes", "Keep steps only in memory", "Share no context", "Avoid testing"], "answer": "Document assumptions and version changes", "skill": "Engineering workflow"},
        {"question": "When a result is unexpected, what should happen first?", "options": ["Investigate inputs and isolate the cause", "Ignore it", "Change many things at once", "Publish it immediately"], "answer": "Investigate inputs and isolate the cause", "skill": "Debugging"},
        {"question": "What makes a technical solution maintainable for a team?", "options": ["Clear structure, tests, and documentation", "Undocumented shortcuts", "One very large file", "Hidden configuration"], "answer": "Clear structure, tests, and documentation", "skill": "Code quality"},
        {"question": "Before releasing a change, what is the most useful check?", "options": ["Test it against defined acceptance criteria", "Assume it works", "Only test the happy path", "Wait for users to report issues"], "answer": "Test it against defined acceptance criteria", "skill": "Quality assurance"},
        {"question": "How should sensitive or production data be handled during a task?", "options": ["Use least privilege and approved safeguards", "Share it in public channels", "Copy it to personal storage", "Disable access controls"], "answer": "Use least privilege and approved safeguards", "skill": "Security practice"},
        {"question": "What is the best response when requirements change?", "options": ["Assess impact, clarify priority, and update the plan", "Continue with the old plan silently", "Discard all previous work", "Avoid informing anyone"], "answer": "Assess impact, clarify priority, and update the plan", "skill": "Requirements management"},
        {"question": "Which evidence best supports a technical decision?", "options": ["Measured results and documented trade-offs", "A guess without context", "The loudest opinion", "An unrelated example"], "answer": "Measured results and documented trade-offs", "skill": "Technical judgment"},
        {"question": "What turns a completed task into a portfolio-ready artifact?", "options": ["A clear README, demo, and explanation of decisions", "Only a screenshot", "No description", "Private notes only"], "answer": "A clear README, demo, and explanation of decisions", "skill": "Professional communication"},
        {"question": "When collaborating on a complex task, what reduces delivery risk?", "options": ["Break work into reviewable increments", "Make all changes at once", "Avoid feedback", "Work without a shared plan"], "answer": "Break work into reviewable increments", "skill": "Collaboration"},
    ]
    for question in seed_questions:
        question["question"] = question["question"].replace("a task", f"a {role_text} task")
    return {"questions": seed_questions}


def generate_job_assessment(roles):
    prompt = f"""
Create exactly 10 multiple-choice questions strictly for these confirmed target job roles: {', '.join(roles)}.
Test only shared or directly relevant technical concepts, practical workplace scenarios, tools, and domain skills needed for these roles.
Do not ask about the student's interests, personality, education, or unrelated aptitude.
Return JSON only: {{"questions":[{{"question":"...","options":["...","...","...","..."],"answer":"exact option","skill":"specific competency"}}]}}.
Every question has four options, one correct answer, and a concrete competency label.
"""
    try:
        response = requests.post("http://localhost:11434/api/generate", json={"model": "llama3.2:3b", "prompt": prompt, "stream": False, "format": "json"}, timeout=120)
        response.raise_for_status()
        quiz = json.loads(response.json()["response"])
        questions = quiz.get("questions", [])
        valid = all(isinstance(q, dict) and len(q.get("options", [])) == 4 and q.get("answer") in q.get("options", []) and q.get("skill") for q in questions)
        if len(questions) == 10 and valid:
            return {"questions": questions}
    except (requests.RequestException, ValueError, KeyError, TypeError):
        pass
    return _fallback_questions(roles)


def analyze_performance(student, roles, answers, score, total):
    """Combine answer-level evidence with a role-aware structured roadmap."""
    strengths = sorted({item["skill"] for item in answers if item["correct"]})
    gaps = sorted({item["skill"] for item in answers if not item["correct"]})
    roadmap = build_learning_roadmap(student, roles, gaps)
    prompt = f"""
Assess job readiness for target roles: {', '.join(roles)}. Score: {score}/{total}.
Demonstrated strengths: {', '.join(strengths) or 'None yet'}.
Skill gaps: {', '.join(gaps) or 'None identified'}.
Write a concise evidence-based summary: what is ready, what to prioritise next, and a realistic readiness statement. Do not mention interests.
"""
    try:
        response = requests.post("http://localhost:11434/api/generate", json={"model": "llama3.2:3b", "prompt": prompt, "stream": False}, timeout=60)
        response.raise_for_status()
        summary = response.json().get("response", "").strip()
    except (requests.RequestException, ValueError, KeyError):
        summary = "Your roadmap is based on the competencies demonstrated in this role-specific assessment. Prioritise the highlighted gaps, practise each milestone, and document your work."
    return {"strengths": strengths, "skill_gaps": gaps, "summary": summary, "roadmap": roadmap}
