from django.urls import path
from . import views

urlpatterns = [
    path("", views.choose_targets, name="choose_targets"),
    path("recommend-roles/", views.role_recommendations, name="role_recommendations"),
    path("test/", views.aptitude_test, name="assessment_test"),
    path("history/", views.assessment_history, name="assessment_history"),
]
