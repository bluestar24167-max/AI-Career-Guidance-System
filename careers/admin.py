from django.contrib import admin
from .models import Career

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "average_salary",
    )

    search_fields = (
        "title",
    )
