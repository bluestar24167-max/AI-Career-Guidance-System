from django.shortcuts import render, redirect, get_object_or_404
from .models import Career
from students.models import Student
from assessment.models import Assessment
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

    ai_response = assessment.report
    analysis = assessment.analysis or {}
    roadmap = analysis.get("roadmap", {})

    return render(
        request,
        "careers/recommendation.html",
        {
            "student": student,
            "assessment": assessment,
            "ai_response": ai_response,
            "analysis": analysis,
            "roadmap": roadmap,
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

    return download_pdf(student, assessment, assessment.report)
