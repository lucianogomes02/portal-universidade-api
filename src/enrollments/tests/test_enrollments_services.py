from unittest.mock import Mock

from django.test import TestCase
from rest_framework import status

from src.courses.repository.course_repository import CourseRepository
from src.enrollments.models import Enrollment
from src.enrollments.service.services import EnrollmentService
from src.users.repository.professor_repository import ProfessorRepository
from src.users.repository.student_repository import StudentRepository


class EnrollmentServiceTestCase(TestCase):
    def setUp(self):
        self.professor = ProfessorRepository().save(
            {
                "name": "Test Professor",
                "email": "professortest@example.com",
                "password": "1234",
                "birth_date": "2000-01-01",
            }
        )

        self.course_data = {
            "name": "Course Test",
            "professor": self.professor.id,
            "workload": 100,
        }

        self.course = CourseRepository().save(
            {
                "name": "Course Test",
                "professor": self.professor,
                "workload": 100,
            }
        )

        self.student = StudentRepository().save(
            {
                "name": "Test Student",
                "email": "studenttest@example.com",
                "password": "1234",
                "birth_date": "2000-01-01",
            }
        )

        self.enrollment_data = {
            "student_id": self.student.id,
            "course_id": self.course.id,
        }

    def test_enroll_student_to_course(self):
        EnrollmentRepository = Mock()
        self.enrollment_repository = EnrollmentRepository

        self.enrollment_repository.return_value.save.return_value = Enrollment(
            **self.enrollment_data
        )

        response = EnrollmentService.enroll_student_to_course(**self.enrollment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data.get("success"),
            f"Aluno {self.student.name} matrículado à Disciplina {self.course.name} com sucesso",
        )

    def test_must_fail_to_enroll_due_student_is_already_enrolled_to_course(self):
        EnrollmentRepository = Mock()
        self.enrollment_repository = EnrollmentRepository

        self.enrollment_repository.return_value.save.return_value = Enrollment(
            **self.enrollment_data
        )

        EnrollmentService.enroll_student_to_course(**self.enrollment_data)

        response = EnrollmentService.enroll_student_to_course(**self.enrollment_data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data.get("error"),
            f"Aluno {self.student.name} já está matrículado à Disciplina {self.course.name}",
        )
