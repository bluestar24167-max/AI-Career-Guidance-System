import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from ai_engine.assessment_engine import analyze_performance, generate_job_assessment
from ai_engine.job_recommendations import recommend_roles
from assessment.models import Assessment
from students.models import Student

POPULAR_ROLES = ["AI Engineer", "Backend Developer", "Cloud Engineer", "Cybersecurity Analyst", "Data Analyst", "Data Scientist", "DevOps Engineer", "Frontend Developer", "Full Stack Developer", "Machine Learning Engineer", "Product Designer", "QA Engineer", "Software Engineer", "UX Designer"]


def _student_or_login(request):
    student_id = request.session.get("student_id")
    return get_object_or_404(Student, id=student_id) if student_id else None


def _clean_roles(raw_roles):
    roles, seen = [], set()
    for role in raw_roles:
        cleaned, key = " ".join(str(role).split()).strip(), " ".join(str(role).split()).strip().casefold()
        if cleaned and len(cleaned) <= 100 and key not in seen:
            roles.append(cleaned)
            seen.add(key)
    return roles[:8]


def choose_targets(request):
    student = _student_or_login(request)
    if not student:
        return redirect("/login/")
    if request.method == "POST":
        roles = _clean_roles(request.POST.getlist("target_roles"))
        if not roles:
            return render(request, "assessment/roles.html", {"student": student, "popular_roles": POPULAR_ROLES, "error": "Choose or add at least one target role."})
        student.target_roles = roles
        student.save(update_fields=["target_roles"])
        request.session["confirmed_target_roles"] = roles
        return redirect("assessment_test")
    return render(request, "assessment/roles.html", {"student": student, "popular_roles": POPULAR_ROLES})


@require_POST
def role_recommendations(request):
    student = _student_or_login(request)
    if not student:
        return JsonResponse({"error": "Please log in again."}, status=401)
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request."}, status=400)
    current_roles = payload.get("current_roles", [])
    if not isinstance(current_roles, list):
        return JsonResponse({"error": "Current roles must be a list."}, status=400)
    return JsonResponse(recommend_roles(str(payload.get("interests", student.interests or ""))[:1000], _clean_roles(current_roles)))


def aptitude_test(request):
    student = _student_or_login(request)
    if not student:
        return redirect("/login/")
    roles = _clean_roles(request.session.get("confirmed_target_roles", student.target_roles))
    if not roles:
        return redirect("choose_targets")
    if request.method == "GET":
        quiz = generate_job_assessment(roles)
        request.session["job_quiz"] = quiz
        request.session["confirmed_target_roles"] = roles
        return render(request, "assessment/test.html", {"roles": roles, "questions": quiz["questions"]})
    quiz = request.session.get("job_quiz")
    if not quiz:
        return redirect("choose_targets")
    answers, score = [], 0
    for index, question in enumerate(quiz.get("questions", [])):
        selected = request.POST.get(f"q{index}", "")
        correct = selected == question.get("answer")
        score += int(correct)
        answers.append({"question": question.get("question", ""), "skill": question.get("skill", "Role competency"), "selected": selected, "correct": correct})
    analysis = analyze_performance(student, roles, answers, score, len(answers))
    assessment = Assessment.objects.create(student=student, target_roles=roles, score=score, total_questions=len(answers), answers=answers, analysis=analysis, report=analysis["summary"])
    request.session.pop("job_quiz", None)
    return render(request, "assessment/result.html", {"student": student, "assessment": assessment, "analysis": analysis})


def assessment_history(request):
    student = _student_or_login(request)
    if not student:
        return redirect("/login/")
    return render(request, "assessment/history.html", {"student": student, "assessments": Assessment.objects.filter(student=student).order_by("-id")})
