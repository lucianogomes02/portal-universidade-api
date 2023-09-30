import uuid

from django.db import models

from src.users.models import Professor, Student


class Course(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100)
    workload = models.PositiveIntegerField()
    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name="professors_courses"
    )
    students = models.ManyToManyField(Student, related_name="students_courses")

    def __str__(self):
        return self.name
