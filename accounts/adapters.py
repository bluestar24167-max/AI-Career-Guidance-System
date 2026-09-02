from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from students.models import Student


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        """
        Connect Google authentication with the existing Student model.
        """

        # Only handle Google login
        if sociallogin.account.provider != "google":
            return

        # Get user information from Google
        email = sociallogin.user.email
        full_name = sociallogin.user.get_full_name()

        if not email:
            return

        try:
            # Check if this student already exists
            student = Student.objects.get(email=email)

        except Student.DoesNotExist:
            # Create a new Student automatically
            student = Student.objects.create(
                full_name=full_name if full_name else email.split("@")[0],
                email=email,
                password=""
            )

        # Store student information temporarily
        request.session["google_student_id"] = student.id
        request.session["google_student_name"] = student.full_name