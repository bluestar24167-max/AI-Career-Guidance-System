from django.shortcuts import render
from students.models import Student
from assessment.models import Assessment


def admin_dashboard(request):

    students = Student.objects.all()

    assessments = Assessment.objects.all()

    return render(
        request,
        "adminpanel/dashboard.html",
        {
            "students": students,
            "assessments": assessments,
            "student_count": students.count(),
            "assessment_count": assessments.count(),
        }
    )
