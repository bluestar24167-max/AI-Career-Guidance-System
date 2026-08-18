from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "education",
        "college",
        "branch",
        "phone",
        "city",
    )

    search_fields = (
        "full_name",
        "email",
        "college",
        "branch",
    )