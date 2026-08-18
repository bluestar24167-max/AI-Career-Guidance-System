from django.db import models

class Career(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    required_skills = models.TextField()
    average_salary = models.CharField(max_length=50)

    def __str__(self):
        return self.title