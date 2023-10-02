from typing import Dict, Optional
from uuid import UUID

from django.db.models import QuerySet

from src.enrollments.models import Enrollment
from src.libs.repository import Repository


class EnrollmentRepository(Repository):
    def __init__(self):
        self.enrollment = Enrollment

    def search_all_objects(self) -> QuerySet[Enrollment]:
        return self.enrollment.objects.all()

    def search_by_id(self, enrollment_id: UUID) -> Enrollment:
        return self.enrollment.objects.filter(id=enrollment_id).first()

    def search_by_student(self, student_id: UUID) -> QuerySet[Enrollment]:
        return self.enrollment.objects.filter(student=student_id)

    def search_by_course(self, course_id: UUID) -> QuerySet[Enrollment]:
        return self.enrollment.objects.filter(course=course_id)

    def search_by_student_and_course(
        self, student_id: UUID, course_id: UUID
    ) -> QuerySet[Enrollment]:
        return self.enrollment.objects.filter(student=student_id, course=course_id)

    def save(self, enrollment_data: Dict) -> Enrollment:
        enrollment = Enrollment.objects.create(
            student=enrollment_data.get("student"),
            course=enrollment_data.get("course"),
        )
        enrollment.save()
        return enrollment

    def update(
        self, enrollment: Enrollment, updated_data: Optional[Dict] = None
    ) -> Enrollment:
        if updated_data:
            for key, value in updated_data.items():
                if hasattr(enrollment, key) and getattr(enrollment, key) != value:
                    setattr(enrollment, key, value)
        enrollment.save()
        return enrollment

    def delete(self, enrollment: Enrollment):
        return enrollment.delete()
