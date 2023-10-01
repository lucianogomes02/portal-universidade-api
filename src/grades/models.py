import uuid

from django.db import models

from src.courses.models import Course
from src.users.models import Professor, Student


class Grade(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="courses_grades", editable=False
    )
    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        related_name="professors_grades",
        editable=False,
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="students_grades",
        editable=False,
    )
    value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.course} - {self.value}"
