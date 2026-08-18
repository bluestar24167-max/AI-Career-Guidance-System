from django.shortcuts import render, redirect, get_object_or_404
from .models import Career
from students.models import Student
from assessment.models import Assessment
from ai_engine.ollama import get_career_recommendation
from .pdf_report import download_pdf


def career_list(request):

    careers = Career.objects.all()

    return render(
        request,
        "careers/list.html",
        {
            "careers": careers
        }
    )


def career_detail(request, career_id):

    career = get_object_or_404(
        Career,
        id=career_id
    )

    return render(
        request,
        "careers/detail.html",
        {
            "career": career
        }
    )


def recommend_career(request):

    if "student_id" not in request.session:
        return redirect("/login/")

    student = Student.objects.get(
        id=request.session["student_id"]
    )

    assessment = Assessment.objects.filter(
        student=student
    ).order_by("-id").first()

    if not assessment:

        return render(
            request,
            "careers/recommendation.html",
            {
                "error": "Please complete the aptitude test first."
            }
        )

    score = f"{assessment.score}/{assessment.total_questions}"

    ai_response = get_career_recommendation(
        student,
        score
    )

    return render(
        request,
        "careers/recommendation.html",
        {
            "student": student,
            "assessment": assessment,
            "ai_response": ai_response
        }
    )


def download_report(request):

    if "student_id" not in request.session:
        return redirect("/login/")

    student = Student.objects.get(
        id=request.session["student_id"]
    )

    assessment = Assessment.objects.filter(
        student=student
    ).order_by("-id").first()

    if not assessment:
        return redirect("/assessment/")

    score = f"{assessment.score}/{assessment.total_questions}"

    ai_response = get_career_recommendation(
        student,
        score
    )

    return download_pdf(
        student,
        assessment,
        ai_response
    )