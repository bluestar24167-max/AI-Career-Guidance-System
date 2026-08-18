from django.urls import path
from . import views

urlpatterns = [
    path("", views.career_list, name="career_list"),
    path("<int:career_id>/", views.career_detail, name="career_detail"),
    path("recommend/", views.recommend_career, name="recommend_career"),
    path(
    "download-report/",
    views.download_report,
    name="download_report"
),
] 