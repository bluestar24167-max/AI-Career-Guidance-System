from django.contrib import admin
from .models import Assessment


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "role",
        "score",
        "created_at"
    )