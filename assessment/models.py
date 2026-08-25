from django.db import models
from students.models import Student


class Assessment(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    target_roles = models.JSONField(default=list)

    score = models.IntegerField()

    total_questions = models.IntegerField()

    report = models.TextField()

    answers = models.JSONField(default=list)

    analysis = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.roles_label}"

    @property
    def roles_label(self):
        return ", ".join(self.target_roles)
