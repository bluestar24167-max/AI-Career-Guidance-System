from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from accounts import views


urlpatterns = [

    # Home
    path("", views.home, name="home"),

    # Authentication
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_page, name="logout"),

    # Google Login Completion
    path(
        "google-login-complete/",
        views.google_login_complete,
        name="google_login_complete"
    ),

    # Student
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),

    # Apps
    path("assessment/", include("assessment.urls")),
    path("careers/", include("careers.urls")),

    # Django Admin
    path("admin/", admin.site.urls),

    # Admin Panel
    path(
        "admin-dashboard/",
        include("adminpanel.urls")
    ),

    # Django Allauth URLs
    path("accounts/", include("allauth.urls")),

    # Service Worker
    path(
        "service-worker.js",
        TemplateView.as_view(
            template_name="service-worker.js",
            content_type="application/javascript",
        ),
        name="service-worker",
    ),
]