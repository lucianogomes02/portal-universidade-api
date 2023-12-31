from typing import Dict, Optional
from uuid import UUID

from django.db.models import QuerySet

from src.libs.repository import Repository
from src.courses.models import Course
from src.users.models import Student


class CourseRepository(Repository):
    def __init__(self):
        self.course = Course

    def search_all_objects(self) -> QuerySet[Course]:
        return self.course.objects.all()

    def search_by_id(self, course_id: UUID) -> Course:
        return self.course.objects.filter(id=course_id).first()

    def search_by_id_and_professor(self, course_id: UUID, professor_id: UUID) -> Course:
        return self.course.objects.filter(id=course_id, professor=professor_id).first()

    def save(self, course_data: Dict) -> Course:
        course = Course.objects.create(
            name=course_data.get("name"),
            workload=course_data.get("workload"),
            professor=course_data.get("professor"),
        )
        if course_data.get("students"):
            course.students.set(course_data.get("students"))
        course.save()
        return course

    def update(self, course: Course, updated_data: Optional[Dict] = None) -> Course:
        if updated_data:
            for key, value in updated_data.items():
                if hasattr(course, key) and getattr(course, key) != value:
                    setattr(course, key, value)
        course.save()
        return course

    def delete(self, course: Course):
        course.delete()
