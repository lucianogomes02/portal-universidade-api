from uuid import UUID

from django.db.models import QuerySet

from src.courses.models import Course
from src.libs.strategies import EntityFilterBasedOnUserTypeStrategy


class FilterCourseByStudent(EntityFilterBasedOnUserTypeStrategy):
    @staticmethod
    def filter_entity_based_user_type(student_id: UUID, queryset: QuerySet[Course]):
        return queryset.filter(students__id=student_id)


class FilterCourseByProfessor(EntityFilterBasedOnUserTypeStrategy):
    @staticmethod
    def filter_entity_based_user_type(professor_id: UUID, queryset: QuerySet[Course]):
        return queryset.filter(professor=professor_id)
