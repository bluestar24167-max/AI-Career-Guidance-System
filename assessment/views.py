from django.shortcuts import render, redirect
from students.models import Student
from assessment.models import Assessment
from ai_engine.category_generator import generate_categories
from ai_engine.role_generator import generate_roles
from ai_engine.quiz_generator import generate_quiz
from ai_engine.report_generator import generate_report
from urllib.parse import unquote


def choose_category(request):

    if "student_id" not in request.session:
        return redirect("/login/")

    student = Student.objects.get(id=request.session["student_id"])

    try:
        data = generate_categories(student)

        return render(
            request,
            "assessment/categories.html",
            {
                "student": student,
                "categories": data["categories"]
            }
        )

    except Exception as e:

        return render(
            request,
            "assessment/categories.html",
            {
                "error": str(e)
            }
        )


def choose_role(request, category):

    if "student_id" not in request.session:
        return redirect("/login/")

    category = unquote(category)

    student = Student.objects.get(id=request.session["student_id"])

    data = generate_roles(student, category)

    return render(
        request,
        "assessment/roles.html",
        {
            "category": category,
            "roles": data["roles"]
        }
    )

def aptitude_test(request, role):

    # Decode URL-encoded role names (e.g. UI%2FUX%20Designer → UI/UX Designer)
    role = unquote(role)

    if "student_id" not in request.session:
        return redirect("/login/")

    student = Student.objects.get(id=request.session["student_id"])

    if request.method == "GET":

        quiz = generate_quiz(student, role)

        request.session["quiz"] = quiz
        request.session["selected_role"] = role

        return render(
            request,
            "assessment/test.html",
            {
                "role": role,
                "questions": quiz["questions"]
            }
        )

    quiz = request.session.get("quiz")

    if not quiz:
        return redirect("/assessment/")

    score = 0

    for index, question in enumerate(quiz["questions"]):

        student_answer = request.POST.get(f"q{index}")

        if student_answer == question["answer"]:
            score += 1

    report = generate_report(
        student,
        role,
        score,
        len(quiz["questions"])
    )

    Assessment.objects.create(
        student=student,
        category="",
        role=role,
        score=score,
        total_questions=len(quiz["questions"]),
        report=report
    )

    return render(
        request,
        "assessment/result.html",
        {
            "student": student,
            "role": role,
            "score": score,
            "total": len(quiz["questions"]),
            "report": report
        }
    )
def assessment_history(request):

    if "student_id" not in request.session:
        return redirect("/login/")

    student = Student.objects.get(id=request.session["student_id"])

    assessments = Assessment.objects.filter(
        student=student
    ).order_by("-id")

    return render(
        request,
        "assessment/history.html",
        {
            "student": student,
            "assessments": assessments
        }
    )