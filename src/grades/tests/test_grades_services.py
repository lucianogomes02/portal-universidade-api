from unittest.mock import Mock

from django.test import TestCase
from rest_framework import status

from src.courses.repository.course_repository import CourseRepository
from src.enrollments.repository.enrollment_repository import EnrollmentRepository
from src.grades.models import Grade
from src.grades.service.grade.services import GradeService
from src.users.repository.professor_repository import ProfessorRepository
from src.users.repository.student_repository import StudentRepository


class GradeServiceTestCase(TestCase):
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

        self.student = StudentRepository().save(
            {
                "name": "Test Student",
                "email": "studenttest@example.com",
                "password": "1234",
                "birth_date": "2000-01-01",
            }
        )

        self.enrollment = EnrollmentRepository().save(
            {"student": self.student, "course": self.course}
        )

        self.grade_data = {
            "student": self.student.id,
            "professor": self.professor.id,
            "course": self.course.id,
            "value": 10.0,
        }

    def test_register_grade(self):
        GradeRepository = Mock()
        self.grade_repository = GradeRepository
        grade_data = {
            "student": self.student,
            "professor": self.professor,
            "course": self.course,
            "value": 10.0,
        }

        self.grade_repository.return_value.save.return_value = Grade(**grade_data)

        response = GradeService.register_grade(self.grade_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data.get("message"),
            "Nota regsitrada com sucesso",
        )

    def test_must_fail_to_register_grade_due_student_has_already_a_grade_in_selected_course(
        self,
    ):
        GradeRepository = Mock()
        self.grade_repository = GradeRepository
        grade_data = {
            "student": self.student,
            "professor": self.professor,
            "course": self.course,
            "value": 10.0,
        }

        self.grade_repository.return_value.save.return_value = Grade(**grade_data)

        GradeService.register_grade(self.grade_data)

        response = GradeService.register_grade(self.grade_data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data.get("message"),
            f"Nota do Aluno já foi registada para a Disciplina {self.course.name}",
        )
