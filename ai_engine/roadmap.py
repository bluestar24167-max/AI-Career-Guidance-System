"""Curated, role-aware learning roadmaps used by the recommendation screen.

The links deliberately point to providers' own learning pages so a student is
not sent to an unverified blog or a disappearing video link.
"""

from urllib.parse import quote_plus


RESOURCE_LIBRARY = {
    "web": [
        ("HTML & CSS foundations", "Build accessible pages, layouts and responsive components.", "MDN Learn", "https://developer.mozilla.org/en-US/docs/Learn"),
        ("JavaScript essentials", "Learn variables, functions, DOM events and asynchronous requests.", "javascript.info", "https://javascript.info/"),
        ("React fundamentals", "Create component-based interfaces and manage application state.", "React Learn", "https://react.dev/learn"),
        ("Version control with Git", "Use branches, commits and pull requests for a portfolio project.", "GitHub Skills", "https://skills.github.com/"),
    ],
    "backend": [
        ("Python foundations", "Write functions, work with collections, errors and virtual environments.", "Python Tutorial", "https://docs.python.org/3/tutorial/"),
        ("Web and APIs", "Build REST endpoints, validate input and understand HTTP status codes.", "MDN Web APIs", "https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Client-side_APIs/Introduction"),
        ("Django", "Create models, views, templates, authentication and a CRUD application.", "Django Tutorial", "https://docs.djangoproject.com/en/stable/intro/tutorial01/"),
        ("Databases and deployment", "Use SQL, PostgreSQL basics and deploy a documented project.", "PostgreSQL Tutorial", "https://www.postgresql.org/docs/current/tutorial.html"),
    ],
    "data": [
        ("Spreadsheets and data thinking", "Clean data, use formulas, pivots and explain basic metrics.", "Microsoft Learn", "https://learn.microsoft.com/en-us/training/browse/?products=excel"),
        ("SQL", "Query, filter, join and aggregate data from relational databases.", "SQLBolt", "https://sqlbolt.com/"),
        ("Python for data", "Use pandas and notebooks to clean, explore and visualise data.", "Kaggle Learn", "https://www.kaggle.com/learn"),
        ("Dashboard and portfolio", "Present a business question, analysis and dashboard in one case study.", "Tableau Learning", "https://www.tableau.com/learn/training"),
    ],
    "ml": [
        ("Python and statistics", "Refresh Python, probability, descriptive statistics and visualisation.", "Kaggle Learn", "https://www.kaggle.com/learn"),
        ("Machine-learning workflow", "Split data, train baselines, evaluate metrics and avoid leakage.", "scikit-learn Guide", "https://scikit-learn.org/stable/getting_started.html"),
        ("Deep learning basics", "Understand tensors, neural networks and a complete training loop.", "PyTorch Tutorials", "https://docs.pytorch.org/tutorials/"),
        ("Applied ML project", "Ship a documented model with a reproducible notebook and clear limitations.", "Google ML Crash Course", "https://developers.google.com/machine-learning/crash-course"),
    ],
    "design": [
        ("UX research", "Write problem statements, interview users and turn findings into requirements.", "UX Design Institute", "https://www.uxdesigninstitute.com/blog/ux-design-resources/"),
        ("Visual design fundamentals", "Practise hierarchy, typography, colour and spacing systems.", "Figma Learn", "https://help.figma.com/hc/en-us/categories/360002051613-Learn-design"),
        ("Wireframes and prototypes", "Create user flows, interactive prototypes and responsive screens.", "Figma Tutorials", "https://www.figma.com/resource-library/"),
        ("Case study portfolio", "Explain the problem, decisions, tests and final outcome of a design.", "NN/g UX Articles", "https://www.nngroup.com/articles/"),
    ],
    "security": [
        ("Networking and Linux", "Understand TCP/IP, DNS, HTTP, permissions and shell navigation.", "Cisco Networking Academy", "https://www.netacad.com/courses/networking-basics"),
        ("Security foundations", "Learn threats, authentication, cryptography and risk basics.", "ISC2 Certified in Cybersecurity", "https://www.isc2.org/certifications/cc"),
        ("Hands-on security labs", "Practise legal web, Linux and network challenges in a sandbox.", "TryHackMe", "https://tryhackme.com/paths"),
        ("Secure application project", "Document a threat model and fix common web vulnerabilities.", "OWASP Top 10", "https://owasp.org/www-project-top-ten/"),
    ],
    "general": [
        ("Role fundamentals", "Learn the vocabulary, core workflow and entry-level expectations for your role.", "Coursera Career Academy", "https://www.coursera.org/career-academy"),
        ("Professional tools", "Practise the tools most often requested in entry-level job descriptions.", "LinkedIn Learning", "https://www.linkedin.com/learning/"),
        ("Portfolio project", "Complete one focused project that demonstrates a real job skill.", "GitHub Skills", "https://skills.github.com/"),
        ("Interview preparation", "Turn your projects into concise stories and practise common questions.", "Big Interview Blog", "https://resources.biginterview.com/"),
    ],
}


def _track_for(role):
    role = (role or "").lower()
    if any(word in role for word in ("machine learning", "data scientist", "ai engineer", "artificial intelligence")):
        return "ml"
    if any(word in role for word in ("data", "business analyst", "bi analyst")):
        return "data"
    if any(word in role for word in ("ui", "ux", "graphic", "product designer")):
        return "design"
    if any(word in role for word in ("cyber", "security", "ethical hacker")):
        return "security"
    if any(word in role for word in ("backend", "django", "python developer", "java developer", "software engineer")):
        return "backend"
    if any(word in role for word in ("front", "web", "react", "full stack", "fullstack")):
        return "web"
    return "general"


def build_learning_roadmap(student, roles, skill_gaps=None):
    """Return a practical, role-aware roadmap with trusted learning resources."""
    roles = roles if isinstance(roles, list) else [roles]
    role_label = ", ".join(roles)
    track = _track_for(role_label)
    current_skills = [skill.strip() for skill in (student.skills or "").split(",") if skill.strip()]
    lessons = []
    for number, (title, outcome, provider, url) in enumerate(RESOURCE_LIBRARY[track], start=1):
        lessons.append({
            "number": number,
            "title": title,
            "outcome": outcome,
            "provider": provider,
            "url": url,
            "duration": "Weeks %s-%s" % ((number - 1) * 4 + 1, number * 4),
            "instructions": "Study the linked material, complete one hands-on exercise, then add a short note or demo to your portfolio.",
            "project": f"Create a small {role_label} portfolio artifact that demonstrates this milestone.",
        })

    role_query = quote_plus(role_label or "entry level career")
    return {
        "track": track,
        "lessons": lessons,
        "current_skills": current_skills,
        "skill_gaps": skill_gaps or [],
        "weekly_plan": "Study 6–8 hours each week: learn for 3 hours, practise for 3 hours, then document progress for 1–2 hours.",
        "job_search_url": f"https://www.linkedin.com/jobs/search/?keywords={role_query}",
    }
