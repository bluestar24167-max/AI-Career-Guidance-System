from django import forms
from .models import Student


class StudentRegistrationForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            "full_name",
            "email",
            "password",
            "education",
            "branch",
            "year",
            "college",
            "city",
            "phone",
            "skills",
            "interests",
            "target_job",
        ]

        widgets = {
            "password": forms.PasswordInput(),

            "education": forms.Select(choices=[
                ("", "Select Education"),
                ("Diploma", "Diploma"),
                ("B.Tech", "B.Tech"),
                ("Degree", "Degree"),
                ("Intermediate", "Intermediate"),
            ]),

            "branch": forms.Select(choices=[
                ("", "Select Branch"),
                ("Computer Engineering", "Computer Engineering"),
                ("Information Technology", "Information Technology"),
                ("Electronics & Communication", "Electronics & Communication"),
                ("Electrical Engineering", "Electrical Engineering"),
                ("Mechanical Engineering", "Mechanical Engineering"),
                ("Civil Engineering", "Civil Engineering"),
            ]),

            "year": forms.Select(choices=[
                ("", "Select Year"),
                ("1st Year", "1st Year"),
                ("2nd Year", "2nd Year"),
                ("3rd Year", "3rd Year"),
                ("Final Year", "Final Year"),
            ]),

            "target_job": forms.Select(choices=[
                ("", "Select Target Job"),
                ("Python Developer", "Python Developer"),
                ("Full Stack Developer", "Full Stack Developer"),
                ("AI Engineer", "AI Engineer"),
                ("Data Analyst", "Data Analyst"),
                ("Data Scientist", "Data Scientist"),
                ("Machine Learning Engineer", "Machine Learning Engineer"),
                ("Cybersecurity Analyst", "Cybersecurity Analyst"),
                ("Cloud Engineer", "Cloud Engineer"),
                ("DevOps Engineer", "DevOps Engineer"),
                ("Software Engineer", "Software Engineer"),
            ]),

            "skills": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Example: Python, HTML, CSS"
            }),

            "interests": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Example: AI, Web Development, Data Science"
            }),
        }