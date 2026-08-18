from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Authentication
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_page, name="logout"),

    # Student
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),

    # Apps
    path("assessment/", include("assessment.urls")),
    path("careers/", include("careers.urls")),

    # Django Admin
    path("admin/", admin.site.urls),

    path(
    "admin-dashboard/",
    include("adminpanel.urls")
),
]