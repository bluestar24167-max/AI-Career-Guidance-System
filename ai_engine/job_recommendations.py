"""AI-powered personalized career role recommendations."""

import json
import requests


FALLBACK_ROLES = [
    {
        "name": "Software Engineer",
        "reason": "Your technical background can support software development and problem-solving roles."
    },
    {
        "name": "Data Analyst",
        "reason": "Your interest in data and analytical skills can be useful for turning information into insights."
    },
    {
        "name": "Cloud Engineer",
        "reason": "Your technical foundation can be developed toward cloud infrastructure and deployment."
    },
    {
        "name": "QA Engineer",
        "reason": "Your technical skills can be applied to software testing, debugging, and quality improvement."
    },
    {
        "name": "Backend Developer",
        "reason": "Your programming and technical interests can support server-side application development."
    },
]


def _fallback_recommendations(profile, current_roles):
    """Return useful recommendations if Ollama is unavailable."""

    selected = {
        str(role).casefold()
        for role in current_roles
    }

    skills = str(profile.get("skills", "")).casefold()
    interests = str(profile.get("interests", "")).casefold()
    education = str(profile.get("education", "")).casefold()
    branch = str(profile.get("branch", "")).casefold()

    profile_text = " ".join([
        skills,
        interests,
        education,
        branch,
    ])

    recommendations = []

    # AI / Machine Learning related profile
    if any(keyword in profile_text for keyword in [
        "ai",
        "artificial intelligence",
        "machine learning",
        "ml",
        "deep learning",
        "data science",
    ]):
        recommendations.extend([
            {
                "name": "AI Engineer",
                "reason": "Your interest or background in AI and machine learning makes this a strong career direction."
            },
            {
                "name": "Machine Learning Engineer",
                "reason": "Your AI and technical interests can lead toward building and deploying machine learning systems."
            },
            {
                "name": "Data Scientist",
                "reason": "Your data and AI interests can be developed into data-driven problem solving and predictive modeling."
            },
        ])

    # Python / programming related profile
    if any(keyword in profile_text for keyword in [
        "python",
        "java",
        "javascript",
        "programming",
        "coding",
        "software",
        "development",
    ]):
        recommendations.extend([
            {
                "name": "Software Engineer",
                "reason": "Your programming background aligns with building, testing, and maintaining software applications."
            },
            {
                "name": "Backend Developer",
                "reason": "Your programming skills can be developed toward APIs, databases, and server-side applications."
            },
            {
                "name": "Full Stack Developer",
                "reason": "Your development interests can support learning both frontend and backend application development."
            },
        ])

    # Data / SQL related profile
    if any(keyword in profile_text for keyword in [
        "sql",
        "database",
        "data",
        "analytics",
        "excel",
        "statistics",
    ]):
        recommendations.extend([
            {
                "name": "Data Analyst",
                "reason": "Your data-related skills and interests align with analyzing information and producing useful insights."
            },
            {
                "name": "Data Scientist",
                "reason": "Your data background can be expanded into statistical analysis and predictive modeling."
            },
        ])

    # Cloud / DevOps related profile
    if any(keyword in profile_text for keyword in [
        "cloud",
        "aws",
        "azure",
        "gcp",
        "devops",
        "docker",
        "kubernetes",
        "linux",
    ]):
        recommendations.extend([
            {
                "name": "Cloud Engineer",
                "reason": "Your infrastructure or cloud interests align with designing and managing cloud-based systems."
            },
            {
                "name": "DevOps Engineer",
                "reason": "Your technical interests can be developed toward automation, deployment, and infrastructure management."
            },
        ])

    # Cybersecurity related profile
    if any(keyword in profile_text for keyword in [
        "cybersecurity",
        "cyber security",
        "security",
        "ethical hacking",
        "network security",
        "penetration testing",
    ]):
        recommendations.append({
            "name": "Cybersecurity Analyst",
            "reason": "Your security interests align with protecting systems, identifying threats, and analyzing vulnerabilities."
        })

    # Remove already selected roles and duplicates
    final_roles = []
    seen = set()

    for role in recommendations:
        key = role["name"].casefold()

        if key not in selected and key not in seen:
            final_roles.append(role)
            seen.add(key)

    # Fill remaining recommendations with general fallback roles
    for role in FALLBACK_ROLES:
        key = role["name"].casefold()

        if key not in selected and key not in seen:
            final_roles.append(role)
            seen.add(key)

    return final_roles[:5]


def recommend_roles(profile, current_roles):
    """
    Generate personalized career role recommendations using the
    student's complete profile.
    """

    selected = {
        str(role).casefold()
        for role in current_roles
    }

    prompt = f"""
You are an AI career adviser helping a student choose suitable career roles.

Analyze the student's complete profile:

Skills:
{profile.get("skills") or "Not provided"}

Interests:
{profile.get("interests") or "Not provided"}

Education:
{profile.get("education") or "Not provided"}

Branch / Specialization:
{profile.get("branch") or "Not provided"}

Year:
{profile.get("year") or "Not provided"}

Experience Level:
{profile.get("experience_level") or "Beginner"}

Existing Target Roles:
{", ".join(profile.get("target_roles", [])) or "None"}

Currently Selected Roles:
{", ".join(current_roles) or "None"}

Recommend 3 to 5 career roles that are genuinely relevant to this student's profile.

Use the student's skills, interests, education, branch, and experience level
to make the recommendations personalized.

Do not simply recommend popular roles.

Do not repeat any currently selected role.

Each recommendation must contain:
- name
- reason

The reason must explain why the role fits this particular student's profile.

Keep each reason under 30 words.

Return JSON only in this exact structure:

{{
    "roles": [
        {{
            "name": "Career Role",
            "reason": "Specific reason based on the student's profile."
        }}
    ]
}}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=45,
        )

        response.raise_for_status()

        data = response.json()

        items = json.loads(
            data["response"]
        ).get("roles", [])

        roles = []

        for item in items:
            if not isinstance(item, dict):
                continue

            name = str(item.get("name", "")).strip()
            reason = str(item.get("reason", "")).strip()

            if not name or not reason:
                continue

            if name.casefold() in selected:
                continue

            roles.append({
                "name": name,
                "reason": reason,
            })

        if roles:
            return {
                "roles": roles[:5]
            }

    except (
        requests.RequestException,
        ValueError,
        KeyError,
        TypeError,
        json.JSONDecodeError,
    ):
        pass

    return {
        "roles": _fallback_recommendations(
            profile,
            current_roles
        )
    }