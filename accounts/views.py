from django.shortcuts import render, redirect
from students.forms import StudentRegistrationForm
from students.models import Student


def home(request):
    return render(request, "home/index.html")


def login_page(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            student = Student.objects.get(email=email, password=password)

            request.session["student_id"] = student.id
            request.session["student_name"] = student.full_name

            return redirect("/dashboard/")

        except Student.DoesNotExist:
            return render(
                request,
                "accounts/login.html",
                {"error": "Invalid Email or Password"}
            )

    return render(request, "accounts/login.html")


def register_page(request):

    if request.method == "POST":

        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/login/")

    else:
        form = StudentRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


def dashboard(request):

    if "student_id" not in request.session:
        return redirect("/login/")

    student = Student.objects.get(id=request.session["student_id"])

    return render(
        request,
        "students/dashboard.html",
        {
            "student": student
        }
    )

def profile(request):

    if "student_id" not in request.session:
        return redirect("/login/")

    student = Student.objects.get(id=request.session["student_id"])

    return render(
        request,
        "students/profile.html",
        {"student": student}
    )
def edit_profile(request):

    if "student_id" not in request.session:
        return redirect("/login/")

    student = Student.objects.get(id=request.session["student_id"])

    if request.method == "POST":

        student.education = request.POST.get("education")
        student.college = request.POST.get("college")
        student.branch = request.POST.get("branch")
        student.phone = request.POST.get("phone")
        student.city = request.POST.get("city")
        student.skills = request.POST.get("skills")
        student.interests = request.POST.get("interests")

        student.save()

        return redirect("/profile/")

    return render(
        request,
        "students/edit_profile.html",
        {"student": student}
    )
def logout_page(request):

    request.session.flush()

    return redirect("/login/")