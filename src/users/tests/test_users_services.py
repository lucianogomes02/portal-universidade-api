from unittest.mock import Mock

from django.test import TestCase
from rest_framework import status

from src.users.models import Coordinator, Student, Professor
from src.users.service.coordinator.services import CoordinatorService
from src.users.service.professor.services import ProfessorService
from src.users.service.student.services import StudentService


class UsersServiceTestCase(TestCase):
    def setUp(self):
        CoordinatorRepository = Mock()
        ProfessorRepository = Mock()
        StudentRepository = Mock()
        self.coordinator_repository = CoordinatorRepository
        self.professor_repository = CoordinatorRepository
        self.student_repository = CoordinatorRepository

    def test_search_for_coordinator(self):
        coordinator_data = {
            "name": "Test Coordinator",
            "email": "coordinatortest@example.com",
            "password": "1234",
            "birth_date": "2000-01-01",
        }

        self.coordinator_repository.return_value.save.return_value = Coordinator(
            **coordinator_data
        )

        coordinator = CoordinatorService.register_coordinator(coordinator_data)

        self.coordinator_repository.return_value.search_by_id.return_value = coordinator

        response = CoordinatorService.search_for_coordinator(
            coordinator_id=coordinator.id
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Test Coordinator")

    def test_register_student(self):
        student_data = {
            "name": "Test Student",
            "email": "studenttest@example.com",
            "password": "1234",
            "birth_date": "2000-01-01",
        }

        self.student_repository.return_value.save.return_value = Student(**student_data)

        response = StudentService.register_student(student_data)

        self.assertTrue(isinstance(response, Student))
        self.assertEqual(response.name, "Test Student")

    def test_unregister_professor(self):
        professor_data = {
            "name": "Test Professor",
            "email": "professortest@example.com",
            "password": "1234",
            "birth_date": "2000-01-01",
        }

        self.professor_repository.return_value.save.return_value = Professor(
            **professor_data
        )

        professor = ProfessorService.register_professor(professor_data)

        self.professor_repository.return_value.search_by_id.return_value = professor

        response = ProfessorService.unregister_professor(professor_id=professor.id)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data["message"], "Professor removido com sucesso")
