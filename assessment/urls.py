from django.urls import path
from . import views

urlpatterns = [
    path("", views.choose_category, name="choose_category"),

    path(
        "roles/<str:category>/",
        views.choose_role,
        name="choose_role"
    ),

    path(
        "test/<str:role>/",
        views.aptitude_test,
        name="aptitude_test"
    ),

    path(
        "history/",
        views.assessment_history,
        name="assessment_history"
    ),
]