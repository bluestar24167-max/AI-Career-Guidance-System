import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from ai_engine.assessment_engine import (
    analyze_performance,
    generate_job_assessment,
)
from ai_engine.job_recommendations import recommend_roles

from assessment.models import Assessment
from students.models import Student


POPULAR_ROLES = [
    "AI Engineer",
    "Backend Developer",
    "Cloud Engineer",
    "Cybersecurity Analyst",
    "Data Analyst",
    "Data Scientist",
    "DevOps Engineer",
    "Frontend Developer",
    "Full Stack Developer",
    "Machine Learning Engineer",
    "Product Designer",
    "QA Engineer",
    "Software Engineer",
    "UX Designer",
]


def _student_or_login(request):
    student_id = request.session.get("student_id")

    return (
        get_object_or_404(Student, id=student_id)
        if student_id
        else None
    )


def _clean_roles(raw_roles):
    """
    Clean role names, remove duplicates, and limit
    an assessment to a maximum of 3 roles.
    """

    roles = []
    seen = set()

    for role in raw_roles:

        cleaned = " ".join(
            str(role).split()
        ).strip()

        key = cleaned.casefold()

        if (
            cleaned
            and len(cleaned) <= 100
            and key not in seen
        ):
            roles.append(cleaned)
            seen.add(key)

    return roles[:3]


def choose_targets(request):
    """
    Display and save the student's selected target roles.
    """

    student = _student_or_login(request)

    if not student:
        return redirect("/login/")

    if request.method == "POST":

        roles = _clean_roles(
            request.POST.getlist("target_roles")
        )

        if not roles:

            return render(
                request,
                "assessment/roles.html",
                {
                    "student": student,
                    "popular_roles": POPULAR_ROLES,
                    "error": (
                        "Choose or add at least one "
                        "target role."
                    ),
                },
            )

        # Save selected roles to the student's profile.
        student.target_roles = roles

        student.save(
            update_fields=["target_roles"]
        )

        # Also keep the roles in the current session.
        request.session[
            "confirmed_target_roles"
        ] = roles

        return redirect("assessment_test")

    return render(
        request,
        "assessment/roles.html",
        {
            "student": student,
            "popular_roles": POPULAR_ROLES,
        },
    )


@require_POST
def role_recommendations(request):
    """
    Generate personalized role recommendations
    using the student's CareerFlow profile.
    """

    student = _student_or_login(request)

    if not student:

        return JsonResponse(
            {
                "error": "Please log in again."
            },
            status=401,
        )

    try:

        payload = json.loads(
            request.body or "{}"
        )

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "error": "Invalid request."
            },
            status=400,
        )

    current_roles = payload.get(
        "current_roles",
        [],
    )

    if not isinstance(
        current_roles,
        list,
    ):

        return JsonResponse(
            {
                "error": "Current roles must be a list."
            },
            status=400,
        )

    # ========================================================
    # BUILD THE STUDENT PROFILE
    # ========================================================
    #
    # job_recommendations.py expects a dictionary and
    # accesses the information using profile.get(...).
    #
    # Previously a string was being sent here, which caused:
    #
    # AttributeError:
    # 'str' object has no attribute 'get'
    #
    # Now we send a proper dictionary.
    # ========================================================

    profile = {
        "skills": student.skills or "",

        "interests": student.interests or "",

        "education": student.education or "",

        "branch": student.branch or "",

        "year": student.year or "",

        "experience_level": (
            student.experience_level
            or "Beginner"
        ),

        "target_roles": _clean_roles(
            current_roles
        ),
    }

    # ========================================================
    # ASK THE AI RECOMMENDATION ENGINE
    # ========================================================

    recommendations = recommend_roles(
        profile,
        _clean_roles(current_roles),
    )

    return JsonResponse(
        recommendations
    )


def aptitude_test(request):
    """
    Generate and process the role-specific assessment.
    """

    student = _student_or_login(request)

    if not student:
        return redirect("/login/")

    # Get the confirmed roles from the session.
    roles = _clean_roles(
        request.session.get(
            "confirmed_target_roles",
            student.target_roles,
        )
    )

    if not roles:
        return redirect("choose_targets")

    # ========================================================
    # START ASSESSMENT
    # ========================================================

    if request.method == "GET":

        quiz = generate_job_assessment(
            roles
        )

        # Store the generated questions in the session
        # so they remain available when the student submits.
        request.session[
            "job_quiz"
        ] = quiz

        request.session[
            "confirmed_target_roles"
        ] = roles

        return render(
            request,
            "assessment/test.html",
            {
                "roles": roles,
                "questions": quiz["questions"],
            },
        )

    # ========================================================
    # SUBMIT ASSESSMENT
    # ========================================================

    quiz = request.session.get(
        "job_quiz"
    )

    if not quiz:
        return redirect("choose_targets")

    questions = quiz.get(
        "questions",
        [],
    )

    # ========================================================
    # ANSWERS
    # ========================================================

    answers = []

    # Combined score is still stored in the existing
    # Assessment.score field for compatibility.
    total_score = 0

    # ========================================================
    # INITIALIZE ROLE SCORES
    # ========================================================

    role_scores = {}

    for role in roles:

        role_scores[role] = {
            "correct": 0,
            "total": 0,
        }

    # ========================================================
    # CHECK EVERY QUESTION
    # ========================================================

    for index, question in enumerate(
        questions
    ):

        selected = request.POST.get(
            f"q{index}",
            "",
        )

        correct_answer = question.get(
            "answer",
            "",
        )

        correct = (
            selected == correct_answer
        )

        # Each generated question now contains
        # the role it belongs to.
        role = question.get(
            "role"
        )

        # Safety fallback for older questions that
        # may not contain the role field.
        if not role:

            role = roles[0]

        # ----------------------------------------------------
        # Make sure role exists in score dictionary
        # ----------------------------------------------------

        if role not in role_scores:

            role_scores[role] = {
                "correct": 0,
                "total": 0,
            }

        # Count this question for that role.
        role_scores[role]["total"] += 1

        # Count correct answer.
        if correct:

            role_scores[role]["correct"] += 1

            total_score += 1

        # ----------------------------------------------------
        # Save detailed answer information
        # ----------------------------------------------------

        answers.append(
            {
                "role": role,

                "question": question.get(
                    "question",
                    "",
                ),

                "skill": question.get(
                    "skill",
                    "Role competency",
                ),

                "selected": selected,

                "correct_answer": (
                    correct_answer
                ),

                "correct": correct,
            }
        )

    # ========================================================
    # CALCULATE ROLE RESULTS
    # ========================================================

    role_results = {}

    for role, result in role_scores.items():

        role_total = result["total"]

        role_correct = result["correct"]

        # Calculate percentage.
        if role_total:

            percentage = round(
                (
                    role_correct
                    / role_total
                )
                * 100
            )

        else:

            percentage = 0

        # ----------------------------------------------------
        # Determine suitability
        # ----------------------------------------------------

        if percentage >= 80:

            suitability = "Excellent"

        elif percentage >= 65:

            suitability = "Strong"

        elif percentage >= 50:

            suitability = "Good"

        elif percentage >= 35:

            suitability = "Developing"

        else:

            suitability = "Needs Improvement"

        role_results[role] = {
            "correct": role_correct,
            "total": role_total,
            "percentage": percentage,
            "suitability": suitability,
        }

    # ========================================================
    # AI PERFORMANCE ANALYSIS
    # ========================================================

    analysis = analyze_performance(
        student,
        roles,
        answers,
        total_score,
        len(questions),
    )

    # Add the separate role results to the AI analysis.
    analysis["role_results"] = role_results

    # ========================================================
    # FIND BEST CURRENT MATCH
    # ========================================================

    if role_results:

        best_role = max(
            role_results,
            key=lambda role:
                role_results[role][
                    "percentage"
                ],
        )

        analysis["best_match"] = {
            "role": best_role,

            "percentage": role_results[
                best_role
            ]["percentage"],

            "suitability": role_results[
                best_role
            ]["suitability"],
        }

    else:

        analysis["best_match"] = None

    # ========================================================
    # SAVE ASSESSMENT
    # ========================================================

    assessment = Assessment.objects.create(
        student=student,

        target_roles=roles,

        score=total_score,

        total_questions=len(questions),

        answers=answers,

        analysis=analysis,

        report=analysis["summary"],
    )

    # ========================================================
    # CLEAR GENERATED QUIZ FROM SESSION
    # ========================================================

    request.session.pop(
        "job_quiz",
        None,
    )

    # ========================================================
    # SHOW RESULT PAGE
    # ========================================================

    return render(
        request,
        "assessment/result.html",
        {
            "student": student,

            "assessment": assessment,

            "analysis": analysis,
        },
    )


def assessment_history(request):
    """
    Display previous assessments for the logged-in student.
    """

    student = _student_or_login(request)

    if not student:
        return redirect("/login/")

    return render(
        request,
        "assessment/history.html",
        {
            "student": student,

            "assessments": (
                Assessment.objects.filter(
                    student=student
                ).order_by("-id")
            ),
        },
    )