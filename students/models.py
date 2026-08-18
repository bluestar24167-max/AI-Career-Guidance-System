from django.db import models


class Student(models.Model):
    full_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=100)

    education = models.CharField(max_length=100, blank=True)

    branch = models.CharField(max_length=100, blank=True)

    year = models.CharField(max_length=30, blank=True)

    college = models.CharField(max_length=150, blank=True)

    city = models.CharField(max_length=100, blank=True)

    phone = models.CharField(max_length=15, blank=True)

    skills = models.TextField(blank=True)

    interests = models.TextField(blank=True)

    target_job = models.CharField(max_length=100, blank=True)

    experience_level = models.CharField(
        max_length=30,
        default="Beginner"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name