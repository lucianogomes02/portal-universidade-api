from typing import Dict, Optional
from uuid import UUID

from django.db.models import QuerySet

from src.grades.models import Grade
from src.libs.repository import Repository


class GradeRepository(Repository):
    def __init__(self):
        self.grade = Grade

    def search_all_objects(self) -> QuerySet[Grade]:
        return self.grade.objects.all()

    def search_by_id(self, grade_id: UUID) -> Grade:
        return self.grade.objects.filter(id=grade_id).first()

    def search_by_student(self, student_id: UUID) -> Grade:
        return self.grade.objects.filter(student=student_id).first()

    def search_by_id_and_student(self, grade_id: UUID, student_id: UUID) -> Grade:
        return self.grade.objects.filter(id=grade_id, student=student_id).first()

    def search_by_student_and_course(self, course_id: UUID, student_id: UUID) -> Grade:
        return self.grade.objects.filter(course=course_id, student=student_id).first()

    def save(self, grade_data: Dict) -> Grade:
        grade = Grade.objects.create(
            course=grade_data.get("course"),
            professor=grade_data.get("professor"),
            student=grade_data.get("student"),
            value=grade_data.get("value"),
        )
        grade.save()
        return grade

    def update(self, grade: Grade, updated_data: Optional[Dict] = None) -> Grade:
        if updated_data:
            for key, value in updated_data.items():
                if hasattr(grade, key) and getattr(grade, key) != value:
                    setattr(grade, key, value)
        grade.save()
        return grade

    def delete(self, grade: Grade):
        grade.delete()
