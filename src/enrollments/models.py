from django.db import models

from src.courses.models import Course
from src.users.models import Student


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
