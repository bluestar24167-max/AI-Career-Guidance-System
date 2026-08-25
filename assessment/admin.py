from django.contrib import admin
from .models import Assessment


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "roles_label",
        "score",
        "created_at"
    )
