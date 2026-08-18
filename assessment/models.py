from django.db import models
from students.models import Student


class Assessment(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    category = models.CharField(max_length=100)

    role = models.CharField(max_length=100)

    score = models.IntegerField()

    total_questions = models.IntegerField()

    report = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.role}"