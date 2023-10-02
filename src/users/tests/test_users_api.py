from unittest.mock import Mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.users.models import User, Coordinator, Professor, Student
from src.users.service.coordinator.services import CoordinatorService
from src.users.service.professor.services import ProfessorService
from src.users.service.student.services import StudentService


class CoordinatorsAPITestCase(APITestCase):
    def setUp(self):
        self.coordinators_list = reverse("Coordinators-list")
        self.super_user = User.objects.create_superuser(
            name="Superuser Test",
            email="superusertest@example.com",
            password="1234",
            username="Superuser Test",
            birth_date="2000-01-01",
        )
        self.client.force_authenticate(self.super_user)

        CoordinatorRepository = Mock()
        self.coordinator_repository = CoordinatorRepository

        coordinator_data = {
            "name": "Test Coordinator",
            "email": "coordinatortest@example.com",
            "password": "1234",
            "birth_date": "2000-01-01",
        }

        self.coordinator_repository.return_value.save.return_value = Coordinator(
            **coordinator_data
        )

        self.coordinator = CoordinatorService.register_coordinator(coordinator_data)

    def test_get_coordinators(self):
        response = self.client.get(self.coordinators_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_coordinators(self):
        coordinator_data = {
            "name": "Coordinator Test 2",
            "email": "coordinatortest2@example.com",
            "password": "1234",
            "birth_date": "2000-01-01",
        }

        response = self.client.post(self.coordinators_list, data=coordinator_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("message"), "Coordenador criado com sucesso")

    def test_put_coordinator(self):
        coordinator_change_data = {
            "email": "emailchanged@example.com",
        }
        response = self.client.put(
            f"/api/coordinators/{self.coordinator.id}/", data=coordinator_change_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("message"), "Coordenador atualizado com sucesso"
        )

    def test_delete_coordinator(self):
        response = self.client.delete(f"/api/coordinators/{self.coordinator.id}/")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(
            response.data.get("message"), "Coordenador removido com sucesso"
        )


class ProfessorsAPITestCase(APITestCase):
    def setUp(self):
        self.professors_list = reverse("Professors-list")
        self.super_user = User.objects.create_superuser(
            name="Superuser Test",
            email="superusertest@example.com",
            password="1234",
            username="Superuser Test",
            birth_date="2000-01-01",
        )
        self.client.force_authenticate(self.super_user)

        ProfessorRepository = Mock()
        self.professor_repository = ProfessorRepository

        professor_data = {
            "name": "Test Professor",
            "email": "professortest@example.com",
            "password": "1234",
            "birth_date": "2000-01-01",
        }

        self.professor_repository.return_value.save.return_value = Professor(
            **professor_data
        )

        self.professor = ProfessorService.register_professor(professor_data)

    def test_get_professors(self):
        response = self.client.get(self.professors_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_professor(self):
        professor_data = {
            "name": "Professor Test 2",
            "email": "professortest2@example.com",
            "password": "1234",
            "birth_date": "2000-01-01",
        }

        response = self.client.post(self.professors_list, data=professor_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("message"), "Professor criado com sucesso")

    def test_put_professor(self):
        professor_change_data = {
            "email": "emailchanged@example.com",
        }
        response = self.client.put(
            f"/api/professors/{self.professor.id}/", data=professor_change_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("message"), "Professor atualizado com sucesso"
        )

    def test_delete_professor(self):
        response = self.client.delete(f"/api/professors/{self.professor.id}/")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data.get("message"), "Professor removido com sucesso")


class StudentsAPITestCase(APITestCase):
    def setUp(self):
        self.students_list = reverse("Students-list")
        self.super_user = User.objects.create_superuser(
            name="Superuser Test",
            email="superusertest@example.com",
            password="1234",
            username="Superuser Test",
            birth_date="2000-01-01",
        )
        self.client.force_authenticate(self.super_user)

        StudentRepository = Mock()
        self.student_repository = StudentRepository

        student_data = {
            "name": "Test Student",
            "email": "studenttest@example.com",
            "password": "1234",
            "birth_date": "2000-01-01",
        }

        self.student_repository.return_value.save.return_value = Student(**student_data)

        self.student = StudentService.register_student(student_data)

    def test_get_students(self):
        response = self.client.get(self.students_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_student(self):
        student_data = {
            "name": "Student Test 2",
            "email": "studenttest2@example.com",
            "password": "1234",
            "birth_date": "2000-01-01",
        }

        response = self.client.post(self.students_list, data=student_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("message"), "Aluno criado com sucesso")

    def test_put_student(self):
        student_change_data = {
            "email": "emailchanged@example.com",
        }
        response = self.client.put(
            f"/api/students/{self.student.id}/", data=student_change_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Aluno atualizado com sucesso")

    def test_delete_student(self):
        response = self.client.delete(f"/api/students/{self.student.id}/")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data.get("message"), "Aluno removido com sucesso")
