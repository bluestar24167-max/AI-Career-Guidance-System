"""
CareerFlow - Dynamic Personalized Career Learning Roadmap

Optimized version.

Flow:

    Selected Role
        ↓
    Student Profile
        ↓
    Assessment Skill Gaps
        ↓
    AI creates complete role framework + weekly stages
        ↓
    Python adds YouTube search links
        ↓
    Python adds trusted practice links
        ↓
    Python adds project reference links
        ↓
    Personalized roadmap

The roadmap is role-agnostic and can support any professional field.
"""

from urllib.parse import quote_plus
import json
import re

from .ollama import generate_response


# ============================================================
# YOUTUBE SEARCH
# ============================================================

def _youtube_search_url(query):
    """
    Create a YouTube search URL for a specific concept.
    """

    return (
        "https://www.youtube.com/results?search_query="
        + quote_plus(str(query or ""))
    )


# ============================================================
# TEXT NORMALISATION
# ============================================================

def _normalise(text):
    """
    Convert text into comparison-friendly format.
    """

    return " ".join(
        str(text or "")
        .lower()
        .replace("-", " ")
        .replace("_", " ")
        .split()
    )


# ============================================================
# STUDENT PROFILE
# ============================================================

def _student_profile(student):
    """
    Extract useful career information from the student.
    """

    if isinstance(student, dict):
        return {
            "education": student.get("education", ""),
            "branch": student.get("branch", ""),
            "year": student.get("year", ""),
            "skills": student.get("skills", ""),
            "interests": student.get("interests", ""),
            "experience_level": (
                student.get("experience_level")
                or "Beginner"
            ),
        }

    return {
        "education": getattr(student, "education", "") or "",
        "branch": getattr(student, "branch", "") or "",
        "year": getattr(student, "year", "") or "",
        "skills": getattr(student, "skills", "") or "",
        "interests": getattr(student, "interests", "") or "",
        "experience_level": (
            getattr(student, "experience_level", "")
            or "Beginner"
        ),
    }


# ============================================================
# JSON CLEANING
# ============================================================

def _clean_json_response(response):
    """
    Clean an Ollama response and extract the JSON object.
    """

    if not response:
        return None

    cleaned = str(response).strip()

    # Remove Markdown code fences.
    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
    )

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1:
        return None

    cleaned = cleaned[start:end + 1]

    try:
        return json.loads(cleaned)

    except (
        json.JSONDecodeError,
        ValueError,
        TypeError,
    ):
        return None


# ============================================================
# TRUSTED PRACTICE RESOURCE
# ============================================================

def _trusted_practice_resource(skill, concepts):
    """
    Return a trusted practice website based on the skill.

    IMPORTANT:

    CareerFlow does NOT allow Ollama to invent practice URLs.

    The AI identifies the required skill.
    CareerFlow chooses an appropriate trusted platform.
    """

    text = _normalise(
        str(skill or "")
        + " "
        + " ".join(
            str(concept or "")
            for concept in (concepts or [])
        )
    )

    # --------------------------------------------------------
    # SQL / DATABASE
    # --------------------------------------------------------

    if any(word in text for word in [
        "sql",
        "mysql",
        "database",
        "postgresql",
        "postgres",
        "sqlite",
        "database management",
    ]):
        return {
            "name": "HackerRank SQL",
            "url": "https://www.hackerrank.com/domains/sql",
        }

    # --------------------------------------------------------
    # PYTHON
    # --------------------------------------------------------

    if "python" in text:
        return {
            "name": "HackerRank Python",
            "url": "https://www.hackerrank.com/domains/python",
        }

    # --------------------------------------------------------
    # JAVASCRIPT
    # --------------------------------------------------------

    if any(word in text for word in [
        "javascript",
        "ecmascript",
    ]):
        return {
            "name": "freeCodeCamp JavaScript",
            "url": (
                "https://www.freecodecamp.org/learn/"
                "javascript-algorithms-and-data-structures-v8/"
            ),
        }

    # --------------------------------------------------------
    # HTML / CSS / FRONTEND
    # --------------------------------------------------------

    if any(word in text for word in [
        "html",
        "css",
        "frontend",
        "front end",
        "web development",
        "responsive design",
    ]):
        return {
            "name": "freeCodeCamp",
            "url": "https://www.freecodecamp.org/learn/",
        }

    # --------------------------------------------------------
    # DATA SCIENCE / DATA ANALYSIS
    # --------------------------------------------------------

    if any(word in text for word in [
        "data science",
        "data analysis",
        "data analytics",
        "pandas",
        "numpy",
        "data visualization",
        "statistics",
    ]):
        return {
            "name": "Kaggle Learn",
            "url": "https://www.kaggle.com/learn",
        }

    # --------------------------------------------------------
    # MACHINE LEARNING / AI
    # --------------------------------------------------------

    if any(word in text for word in [
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "neural network",
        "computer vision",
        "natural language processing",
        "nlp",
        "model training",
        "generative ai",
    ]):
        return {
            "name": "Kaggle Learn",
            "url": "https://www.kaggle.com/learn",
        }

    # --------------------------------------------------------
    # ALGORITHMS / DSA / PROGRAMMING
    # --------------------------------------------------------

    if any(word in text for word in [
        "algorithm",
        "algorithms",
        "data structure",
        "data structures",
        "dsa",
        "problem solving",
        "programming",
        "coding",
    ]):
        return {
            "name": "HackerRank",
            "url": "https://www.hackerrank.com/domains",
        }

    # --------------------------------------------------------
    # GENERAL FALLBACK
    # --------------------------------------------------------

    return {
        "name": "freeCodeCamp",
        "url": "https://www.freecodecamp.org/learn/",
    }


# ============================================================
# PROJECT RESOURCE
# ============================================================

def _project_resource_url(project, skill, concepts):
    """
    Create a project reference/search resource.

    GitHub repository search is used as a reference source
    instead of allowing Ollama to invent a repository URL.
    """

    project_text = str(project or "").strip()

    if not project_text:
        project_text = str(skill or "").strip()

    concepts_text = " ".join(
        str(concept or "")
        for concept in (concepts or [])
    )

    query = (
        f"{project_text} "
        f"{skill or ''} "
        f"{concepts_text}"
    ).strip()

    return (
        "https://github.com/search?q="
        + quote_plus(query)
        + "&type=repositories"
    )


# ============================================================
# AI COMPLETE ROADMAP GENERATION
# ============================================================

def _generate_role_roadmap(
    role,
    student,
    skill_gaps=None,
):
    """
    Generate the complete learning roadmap for ONE role
    using a SINGLE Ollama request.

    This keeps result-generation time lower than making
    a separate AI request for every individual skill.
    """

    profile = _student_profile(student)

    skill_gaps = skill_gaps or []

    gaps_text = ", ".join(
        str(gap)
        for gap in skill_gaps
        if str(gap).strip()
    )

    prompt = f"""
You are the career curriculum architect for CareerFlow.

Create a personalized 8-stage learning roadmap for this
career role.

CAREER ROLE:
{role}

STUDENT PROFILE:

Education:
{profile["education"] or "Not provided"}

Branch / Specialization:
{profile["branch"] or "Not provided"}

Year:
{profile["year"] or "Not provided"}

Current Skills:
{profile["skills"] or "Not provided"}

Interests:
{profile["interests"] or "Not provided"}

Experience Level:
{profile["experience_level"]}

ASSESSMENT SKILL GAPS:
{gaps_text or "No specific gaps provided"}

IMPORTANT:

1. The career role can belong to ANY professional field.

2. Do NOT assume this is a software role.

3. Do NOT add programming unless it is genuinely relevant
   to the selected career.

4. Use the student's education, branch, current skills,
   interests and experience level.

5. Assessment skill gaps should receive higher priority.

6. Begin with foundations and progressively move toward
   practical job-ready skills.

7. Avoid unnecessary degree requirements.

8. Every stage must teach ONE clearly defined skill.

9. Make the sequence logical:

   foundations
   →
   core skills
   →
   practical application
   →
   advanced skills
   →
   project/job readiness

10. Create approximately 8 stages.

11. Each stage should represent roughly one week.

12. Keep the workload realistic.

13. Estimated learning time must be realistic.

14. The YouTube query must be specific to the exact concepts.

15. Do NOT create URLs.

16. Do NOT use Markdown.

17. Do NOT write generic statements such as:
   "learn everything about this field."

18. Practice must actually exercise the skill.

19. Projects must directly relate to the skill.

20. Every project should be specific and realistic.

21. The roadmap must be personalized to this student,
    not a generic roadmap copied for everyone.

22. For the "watch_query", describe exactly what the student
    should search for on YouTube.

23. The "practice" field must describe an actual activity,
    not simply say "practice this skill."

24. The project must be something the student can realistically
    build or complete at their current level.

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "stages": [
        {{
            "skill": "Specific skill name",

            "priority": "High",

            "concepts": [
                "Specific concept 1",
                "Specific concept 2",
                "Specific concept 3"
            ],

            "reason":
                "Why this skill matters for this student and role",

            "goal":
                "What the student should accomplish",

            "learn":
                "What the student should study and understand",

            "watch_query":
                "Specific YouTube search query for these concepts",

            "practice":
                "Specific practical practice activity",

            "tasks": [
                "Practical task 1",
                "Practical task 2",
                "Practical task 3"
            ],

            "project":
                "Specific small realistic project or practical assignment",

            "time":
                "Estimated learning time",

            "outcome":
                "What the student should be able to do after this stage"
        }}
    ]
}}

Priority must be exactly one of:

High
Medium
Low
"""

    try:

        response = generate_response(prompt)

        data = _clean_json_response(response)

        if not isinstance(data, dict):
            return []

        stages = data.get(
            "stages",
            [],
        )

        if not isinstance(stages, list):
            return []

        cleaned_stages = []

        for stage in stages[:8]:

            if not isinstance(stage, dict):
                continue

            skill = str(
                stage.get(
                    "skill",
                    "",
                )
            ).strip()

            if not skill:
                continue

            concepts = stage.get(
                "concepts",
                [],
            )

            if not isinstance(
                concepts,
                list,
            ):
                concepts = []

            concepts = [
                str(concept).strip()
                for concept in concepts
                if str(concept).strip()
            ]

            if not concepts:
                concepts = [skill]

            priority = str(
                stage.get(
                    "priority",
                    "Medium",
                )
            ).strip()

            if priority not in {
                "High",
                "Medium",
                "Low",
            }:
                priority = "Medium"

            tasks = stage.get(
                "tasks",
                [],
            )

            if not isinstance(
                tasks,
                list,
            ):
                tasks = []

            tasks = [
                str(task).strip()
                for task in tasks
                if str(task).strip()
            ]

            cleaned_stages.append(
                {
                    "skill": skill,

                    "priority": priority,

                    "concepts": concepts,

                    "reason": str(
                        stage.get(
                            "reason",
                            "",
                        )
                    ).strip(),

                    "goal": str(
                        stage.get(
                            "goal",
                            "",
                        )
                    ).strip(),

                    "learn": str(
                        stage.get(
                            "learn",
                            "",
                        )
                    ).strip(),

                    "watch_query": str(
                        stage.get(
                            "watch_query",
                            (
                                f"{skill} "
                                f"{' '.join(concepts)} "
                                "tutorial beginners"
                            ),
                        )
                    ).strip(),

                    "practice": str(
                        stage.get(
                            "practice",
                            "",
                        )
                    ).strip(),

                    "tasks": tasks,

                    "project": str(
                        stage.get(
                            "project",
                            "",
                        )
                    ).strip(),

                    "time": str(
                        stage.get(
                            "time",
                            "5–7 days",
                        )
                    ).strip(),

                    "outcome": str(
                        stage.get(
                            "outcome",
                            "",
                        )
                    ).strip(),
                }
            )

        return cleaned_stages

    except Exception:
        return []


# ============================================================
# DYNAMIC ROLE CURRICULUM (works for ANY role)
# ============================================================

def _infer_skill_chapters(role, skill_gaps=None):
    """
    Build a sequential list of learning chapters for ANY role.

    Priority:
      1. Assessment skill gaps (most personalised)
      2. Role-keyword inference (data, backend, design, etc.)
      3. Generic progressive path using the role name

    Returns a list of skill names that become roadmap stages.
    """

    gaps = [
        str(g).strip()
        for g in (skill_gaps or [])
        if str(g).strip()
    ]

    # Deduplicate while preserving order
    seen = set()
    unique_gaps = []
    for g in gaps:
        key = g.casefold()
        if key not in seen:
            seen.add(key)
            unique_gaps.append(g)

    role_lower = _normalise(role)

    # Keyword → chapter banks (skill families, not locked titles)
    banks = {
        "data_science": [
            "Python for data work",
            "Statistics and probability basics",
            "Exploratory data analysis",
            "Machine learning fundamentals",
            "Feature engineering and model evaluation",
            "End-to-end data project",
        ],
        "data_analyst": [
            "SQL fundamentals",
            "Data cleaning and preparation",
            "Business metrics and KPIs",
            "Data visualisation and dashboards",
            "Analysis and storytelling",
            "End-to-end analyst project",
        ],
        "backend": [
            "Programming fundamentals",
            "HTTP, REST APIs and JSON",
            "Backend framework basics",
            "Databases and SQL",
            "Authentication and basic security",
            "Testing and deployment basics",
            "Portfolio backend project",
        ],
        "frontend": [
            "HTML and CSS fundamentals",
            "JavaScript essentials",
            "Responsive design and accessibility",
            "Frontend framework basics",
            "Working with APIs from the client",
            "Frontend portfolio project",
        ],
        "devops_cloud": [
            "Linux and command-line basics",
            "Networking and cloud fundamentals",
            "Containers with Docker",
            "CI/CD pipelines",
            "Infrastructure as code basics",
            "Cloud project and monitoring",
        ],
        "security": [
            "Security fundamentals and threat models",
            "Network and system security basics",
            "Vulnerability assessment basics",
            "Secure coding practices",
            "Incident response fundamentals",
            "Security portfolio project",
        ],
        "design": [
            "Design principles and visual hierarchy",
            "User research and personas",
            "Wireframing and prototyping",
            "UI design and design systems",
            "Usability testing",
            "Design portfolio project",
        ],
        "product": [
            "Product thinking and discovery",
            "User research and problem framing",
            "Roadmapping and prioritisation",
            "Metrics and experimentation",
            "Stakeholder communication",
            "Product case study project",
        ],
        "qa": [
            "Testing fundamentals and types of tests",
            "Test case design",
            "Manual testing workflows",
            "Automation testing basics",
            "Bug reporting and quality metrics",
            "QA portfolio project",
        ],
    }

    inferred = []

    if any(k in role_lower for k in [
        "data scientist", "machine learning", "ml engineer",
        "ai engineer", "deep learning", "artificial intelligence",
    ]):
        inferred = banks["data_science"]
    elif "data analyst" in role_lower or (
        "data" in role_lower and "analyst" in role_lower
    ):
        inferred = banks["data_analyst"]
    elif any(k in role_lower for k in [
        "backend", "software engineer", "software developer",
        "full stack", "fullstack", "api developer",
    ]):
        inferred = banks["backend"]
    elif any(k in role_lower for k in [
        "frontend", "front end", "web developer", "react", "ui developer",
    ]):
        inferred = banks["frontend"]
    elif any(k in role_lower for k in [
        "devops", "cloud", "sre", "platform engineer", "kubernetes",
    ]):
        inferred = banks["devops_cloud"]
    elif any(k in role_lower for k in [
        "security", "cyber", "penetration", "infosec",
    ]):
        inferred = banks["security"]
    elif any(k in role_lower for k in [
        "ux", "ui designer", "product designer", "design",
    ]):
        inferred = banks["design"]
    elif "product" in role_lower and "manager" in role_lower:
        inferred = banks["product"]
    elif any(k in role_lower for k in [
        "qa", "quality assurance", "test engineer", "sdet",
    ]):
        inferred = banks["qa"]

    chapters = []
    used = set()

    for gap in unique_gaps[:5]:
        key = gap.casefold()
        if key not in used:
            chapters.append(gap)
            used.add(key)

    for skill in inferred:
        key = skill.casefold()
        if key not in used:
            chapters.append(skill)
            used.add(key)

    # Pad so custom / unknown roles still get a full path
    generic_pad = [
        f"{role} role overview and core responsibilities",
        f"Essential tools and workflows for {role}",
        f"Foundational skills required for {role}",
        f"Practical problem-solving for {role}",
        f"Intermediate techniques used by {role} professionals",
        f"Portfolio project for {role}",
    ]

    for skill in generic_pad:
        if len(chapters) >= 6:
            break
        key = skill.casefold()
        if key not in used:
            chapters.append(skill)
            used.add(key)

    return chapters[:8]


def _stage_from_skill(role, skill, index, total, is_gap=False):
    """
    Turn one skill/chapter name into a full roadmap stage dict.
    Fully dynamic — no hardcoded role content required.
    """

    skill = str(skill).strip()
    priority = "High" if is_gap or index <= 3 else "Medium"

    if index == 1:
        goal = f"Build a solid foundation in {skill} for the {role} role."
        learn = (
            f"Study the core ideas behind {skill}: key terms, "
            f"why it matters for {role}, and the minimum you must understand."
        )
        practice = (
            f"Complete beginner exercises focused only on {skill}. "
            f"Aim for understanding, not speed."
        )
        project = (
            f"Produce a small artefact that proves you understand "
            f"the basics of {skill}."
        )
    elif index >= total - 1:
        goal = f"Apply {skill} in a realistic mini-project relevant to {role}."
        learn = (
            f"Review how professionals use {skill} on the job and "
            f"what a junior-level deliverable looks like."
        )
        practice = (
            f"Combine {skill} with earlier chapters to solve one "
            f"realistic problem end-to-end."
        )
        project = (
            f"Build a portfolio-ready piece that demonstrates {skill} "
            f"in the context of {role}."
        )
    else:
        goal = f"Become productive with {skill} for day-to-day {role} work."
        learn = (
            f"Go deeper into {skill}: common patterns, typical mistakes, "
            f"and how it connects to other {role} skills."
        )
        practice = (
            f"Solve 3–5 practical exercises that force you to use {skill} "
            f"the way it appears at work."
        )
        project = (
            f"Complete a small practical assignment centred on {skill}."
        )

    concepts = [
        f"{skill} fundamentals",
        f"Practical use of {skill}",
        f"{skill} in {role} workflows",
    ]

    return {
        "skill": skill,
        "priority": priority,
        "concepts": concepts,
        "reason": (
            f"{skill} is a required competency for the {role} role. "
            f"Mastering it early reduces friction in later stages."
            if is_gap
            else f"{skill} is a core building block on the path to becoming job-ready as a {role}."
        ),
        "goal": goal,
        "learn": learn,
        "watch_query": f"{skill} tutorial for beginners {role}",
        "practice": practice,
        "tasks": [
            f"Study the essential concepts of {skill}",
            f"Complete hands-on practice focused on {skill}",
            f"Apply {skill} to a small realistic task",
        ],
        "project": project,
        "time": "5–7 days",
        "outcome": (
            f"You can explain and apply {skill} in practical "
            f"{role}-related situations."
        ),
    }


def _build_dynamic_curriculum(role, skill_gaps=None):
    """
    Generate a complete sequential roadmap for ANY role
    without depending on Ollama.
    """

    chapters = _infer_skill_chapters(role, skill_gaps)
    gap_set = {
        str(g).strip().casefold()
        for g in (skill_gaps or [])
        if str(g).strip()
    }

    stages = []
    total = len(chapters)

    for index, skill in enumerate(chapters, start=1):
        is_gap = skill.casefold() in gap_set
        stages.append(
            _stage_from_skill(
                role,
                skill,
                index,
                total,
                is_gap=is_gap,
            )
        )

    return stages


def _fallback_stage(
    role,
    skill,
    concepts,
):
    """
    Minimal single-stage fallback (last resort only).
    """

    concept_text = ", ".join(concepts)

    return {
        "skill": skill,
        "priority": "High",
        "concepts": concepts,
        "reason": (
            f"{skill} is an important foundation for "
            f"the {role} role."
        ),
        "goal": (
            f"Build a practical understanding of {skill} "
            f"for the {role} role."
        ),
        "learn": (
            f"Study the fundamentals of {skill}, including "
            f"{concept_text}."
        ),
        "watch_query": (
            f"{skill} {concept_text} "
            "tutorial beginners"
        ),
        "practice": (
            f"Complete practical exercises related to "
            f"{skill}, focusing on real-world problems."
        ),
        "tasks": [
            f"Learn the core concepts of {skill}.",
            f"Complete practical exercises involving {skill}.",
            f"Apply {skill} to a small real-world problem.",
        ],
        "project": (
            f"Build a small practical project demonstrating "
            f"{skill}."
        ),
        "time": "5–7 days",
        "outcome": (
            f"You should be able to apply the fundamentals "
            f"of {skill} to practical tasks."
        ),
    }


# ============================================================
# PRIORITY CALCULATION
# ============================================================

def _skill_matches_gap(
    skill,
    skill_gaps,
):
    """
    Check whether an AI-generated skill is related
    to an assessment skill gap.
    """

    if not skill_gaps:
        return False

    skill_text = _normalise(
        skill.get(
            "skill",
            "",
        )
        + " "
        + " ".join(
            skill.get(
                "concepts",
                [],
            )
        )
    )

    for gap in skill_gaps:

        gap_text = _normalise(
            gap
        )

        if not gap_text:
            continue

        gap_words = [
            word
            for word in gap_text.split()
            if len(word) > 2
        ]

        if any(
            word in skill_text
            for word in gap_words
        ):
            return True

    return False


def _priority_for_skill(
    skill,
    skill_gaps,
):
    """
    Determine personalized priority.
    """

    if _skill_matches_gap(
        skill,
        skill_gaps,
    ):
        return "High Priority"

    priority = skill.get(
        "priority",
        "Medium",
    )

    if priority == "High":
        return "High Priority"

    if priority == "Low":
        return "Supporting Skill"

    return "Core Skill"


# ============================================================
# BUILD LEARNING ROADMAP
# ============================================================

def build_learning_roadmap(
    student,
    roles,
    skill_gaps=None,
):
    """
    Build personalized weekly roadmaps.

    PERFORMANCE ARCHITECTURE:

    Old version:

        1 Ollama call for framework
        +
        1 Ollama call per skill

    New version:

        1 Ollama call for the COMPLETE roadmap
        per selected role.

    This keeps the roadmap generation significantly faster.
    """

    # --------------------------------------------------------
    # NORMALISE ROLES
    # --------------------------------------------------------

    if not isinstance(
        roles,
        list,
    ):
        roles = [roles]

    roles = [
        str(role).strip()
        for role in roles
        if str(role).strip()
    ]

    if not roles:
        return []

    skill_gaps = skill_gaps or []

    all_roadmaps = []

    # ========================================================
    # PROCESS EACH ROLE
    # ========================================================

    for role in roles:

        # ----------------------------------------------------
        # ONE AI REQUEST FOR COMPLETE ROLE ROADMAP
        # ----------------------------------------------------

        stages = _generate_role_roadmap(
            role,
            student,
            skill_gaps,
        )

        # ----------------------------------------------------
        # FALLBACK — dynamic curriculum for ANY role
        # ----------------------------------------------------

        if not stages:
            stages = _build_dynamic_curriculum(
                role,
                skill_gaps,
            )

            if not stages:
                stages = [
                    _fallback_stage(
                        role,
                        f"{role} core foundations",
                        [
                            "Role overview",
                            "Essential skills",
                            "Common tools",
                        ],
                    ),
                ]

        # ====================================================
        # BUILD FRONTEND-FRIENDLY ROADMAP
        # ====================================================

        for index, stage in enumerate(
            stages,
            start=1,
        ):

            # ------------------------------------------------
            # SKILL
            # ------------------------------------------------

            skill_name = str(
                stage.get(
                    "skill",
                    f"{role} skill {index}",
                )
            ).strip()

            # ------------------------------------------------
            # CONCEPTS
            # ------------------------------------------------

            concepts = stage.get(
                "concepts",
                [],
            )

            if not isinstance(
                concepts,
                list,
            ):
                concepts = []

            if not concepts:
                concepts = [
                    skill_name
                ]

            # ------------------------------------------------
            # YOUTUBE SEARCH
            # ------------------------------------------------

            watch_query = str(
                stage.get(
                    "watch_query",
                    (
                        f"{skill_name} "
                        f"{' '.join(concepts)} "
                        "tutorial beginners"
                    ),
                )
            ).strip()

            watch_url = _youtube_search_url(
                watch_query
            )

            # ------------------------------------------------
            # PRACTICE RESOURCE
            # ------------------------------------------------

            practice_resource = (
                _trusted_practice_resource(
                    skill_name,
                    concepts,
                )
            )

            # ------------------------------------------------
            # PROJECT
            # ------------------------------------------------

            project_text = str(
                stage.get(
                    "project",
                    "",
                )
            ).strip()

            if not project_text:
                project_text = (
                    f"Build a small practical project "
                    f"using {skill_name}."
                )

            project_url = _project_resource_url(
                project_text,
                skill_name,
                concepts,
            )

            # ------------------------------------------------
            # TASKS
            # ------------------------------------------------

            tasks = stage.get(
                "tasks",
                [],
            )

            if not isinstance(
                tasks,
                list,
            ):
                tasks = []

            tasks = [
                str(task).strip()
                for task in tasks
                if str(task).strip()
            ]

            # ------------------------------------------------
            # FINAL ROADMAP OBJECT
            # ------------------------------------------------

            all_roadmaps.append(
                {
                    "number": index,

                    "week": f"Week {index}",

                    "week_number": index,

                    "role": role,

                    "goal": str(
                        stage.get(
                            "goal",
                            "",
                        )
                    ).strip(),

                    "skill": skill_name,

                    "concepts": concepts,

                    "reason": str(
                        stage.get(
                            "reason",
                            "",
                        )
                    ).strip(),

                    # ----------------------------------------
                    # LEARN
                    # ----------------------------------------

                    "learn": str(
                        stage.get(
                            "learn",
                            "",
                        )
                    ).strip(),

                    # Reserved for future curated learning
                    # resource mapping.
                    "learn_url": "",

                    "learn_provider": "",

                    # ----------------------------------------
                    # WATCH
                    # ----------------------------------------

                    "watch": watch_url,

                    "watch_url": watch_url,

                    "watch_query": watch_query,

                    "watch_provider": "YouTube",

                    # ----------------------------------------
                    # PRACTICE
                    # ----------------------------------------

                    "practice": str(
                        stage.get(
                            "practice",
                            "",
                        )
                    ).strip(),

                    "practice_url": (
                        practice_resource["url"]
                    ),

                    "practice_provider": (
                        practice_resource["name"]
                    ),

                    # ----------------------------------------
                    # TASKS
                    # ----------------------------------------

                    "tasks": tasks,

                    # ----------------------------------------
                    # PROJECT
                    # ----------------------------------------

                    "project": project_text,

                    "project_url": project_url,

                    "project_resource_name": (
                        "GitHub project references"
                    ),

                    # ----------------------------------------
                    # TIME
                    # ----------------------------------------

                    "time": str(
                        stage.get(
                            "time",
                            "5–7 days",
                        )
                    ).strip(),

                    # ----------------------------------------
                    # OUTCOME
                    # ----------------------------------------

                    "outcome": str(
                        stage.get(
                            "outcome",
                            "",
                        )
                    ).strip(),

                    # ----------------------------------------
                    # PRIORITY
                    # ----------------------------------------

                    "priority": _priority_for_skill(
                        stage,
                        skill_gaps,
                    ),
                }
            )

    return all_roadmaps