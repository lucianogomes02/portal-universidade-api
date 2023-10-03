from typing import Dict
from uuid import UUID

from django.contrib.auth.models import Group
from django.db.models import QuerySet

from src.libs.repository import Repository
from src.users.models import Student, User


class StudentRepository(Repository):
    def __init__(self):
        self.student_user = Student

    def search_all_objects(self) -> QuerySet[Student]:
        return self.student_user.objects.all()

    def search_by_id(self, student_id: UUID) -> Student:
        return self.student_user.objects.filter(id=student_id).first()

    def save(self, student_data: Dict) -> Student:
        student_json = {**student_data}
        student = Student.objects.create(
            **student_data,
            username=student_json.get("email"),
            user_type=User.UserType.STUDENT
        )
        student.set_password(student.password)
        student_group = Group.objects.filter(name="StudentGroup").first()
        student.groups.add(student_group)
        student.save()
        return student

    def update(self, student: Student, updated_data: Dict) -> Student:
        for key, value in updated_data.items():
            if hasattr(student, key) and getattr(student, key) != value:
                setattr(student, key, value)

        new_password = updated_data.get("password")
        if new_password:
            student.set_password(new_password)

        student.save()
        return student

    def delete(self, student: Student):
        student.delete()
