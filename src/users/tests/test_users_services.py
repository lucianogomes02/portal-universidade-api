from unittest.mock import Mock

from django.test import TestCase
from rest_framework import status

from src.users.models import Coordinator, Student, Professor
from src.users.repository.coordinator_repository import CoordinatorRepository
from src.users.repository.professor_repository import ProfessorRepository
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
        self.coordinator = CoordinatorRepository().save(
            {
                "name": "Test Coordinator",
                "email": "coordinatortest@example.com",
                "password": "1234",
                "birth_date": "2000-01-01",
            }
        )

        self.coordinator_repository.return_value.search_by_id.return_value = (
            self.coordinator
        )

        response = CoordinatorService.search_for_coordinator(
            coordinator_id=self.coordinator.id
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"]["name"], "Test Coordinator")

    def test_register_student(self):
        student_data = {
            "name": "Test Student",
            "email": "studenttest@example.com",
            "password": "1234",
            "birth_date": "2000-01-01",
        }

        self.student_repository.return_value.save.return_value = Student(**student_data)

        response = StudentService.register_student(student_data)

        self.assertTrue(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["success"], "Aluno cadastrado com sucesso")

    def test_unregister_professor(self):
        self.professor = ProfessorRepository().save(
            {
                "name": "Test Professor",
                "email": "professortest@example.com",
                "password": "1234",
                "birth_date": "2000-01-01",
            }
        )

        self.professor_repository.return_value.search_by_id.return_value = (
            self.professor
        )

        response = ProfessorService.unregister_professor(professor_id=self.professor.id)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data["success"], "Professor removido com sucesso")
