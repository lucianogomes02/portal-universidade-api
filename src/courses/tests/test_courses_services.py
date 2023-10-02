from unittest.mock import Mock

from django.test import TestCase
from rest_framework import status

from src.courses.models import Course
from src.courses.repository.course_repository import CourseRepository
from src.courses.service.course.services import CourseService
from src.users.repository.professor_repository import ProfessorRepository


class CoursesServiceTestCase(TestCase):
    def setUp(self):
        self.professor = ProfessorRepository().save(
            {
                "name": "Test Professor",
                "email": "professortest@example.com",
                "password": "1234",
                "birth_date": "2000-01-01",
            }
        )

        self.course = CourseRepository().save(
            {
                "name": "Course Test",
                "professor": self.professor,
                "workload": 100,
            }
        )

        self.course_data = {
            "name": "Course Test 2",
            "professor": self.professor.id,
            "workload": 100,
        }

    def test_search_for_course(self):
        CourseRepository = Mock()
        self.course_repository = CourseRepository

        self.course_repository.return_value.search_by_id.return_value = self.course

        response = CourseService.search_for_course(course_id=self.course.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"]["name"], "Course Test")

    def test_register_course(self):
        CourseRepository = Mock()
        self.course_repository = CourseRepository

        self.course_repository.return_value.save.return_value = Course(
            **{
                "name": "Course Test 2",
                "professor": self.professor,
                "workload": 100,
            }
        )

        response = CourseService.register_course(self.course_data)

        self.assertTrue(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["success"], "Disciplina cadastrada com sucesso")

    def test_unregister_course(self):
        CourseRepository = Mock()
        self.course_repository = CourseRepository

        self.course_repository.return_value.search_by_id.return_value = self.course

        response = CourseService.unregister_course(course_id=self.course.id)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data["success"], "Disciplina removida com sucesso")
