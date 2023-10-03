from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.users.models import User
from src.users.repository.coordinator_repository import CoordinatorRepository
from src.users.repository.professor_repository import ProfessorRepository
from src.users.repository.student_repository import StudentRepository


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

        self.coordinator = CoordinatorRepository().save(
            {
                "name": "Test Coordinator",
                "email": "coordinatortest@example.com",
                "password": "1234",
                "birth_date": "2000-01-01",
            }
        )

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
        self.assertEqual(
            response.data.get("success"), "Coordenador registrado com sucesso"
        )

    def test_put_coordinator(self):
        coordinator_change_data = {
            "email": "emailchanged@example.com",
        }
        response = self.client.put(
            f"/api/coordinators/{self.coordinator.id}/", data=coordinator_change_data
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(
            response.data.get("success"), "Coordenador alterado com sucesso"
        )

    def test_delete_coordinator(self):
        response = self.client.delete(f"/api/coordinators/{self.coordinator.id}/")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(
            response.data.get("success"), "Coordenador removido com sucesso"
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

        self.professor = ProfessorRepository().save(
            {
                "name": "Test Professor",
                "email": "professortest@example.com",
                "password": "1234",
                "birth_date": "2000-01-01",
            }
        )

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
        self.assertEqual(
            response.data.get("success"), "Professor cadastrado com sucesso"
        )

    def test_put_professor(self):
        professor_change_data = {
            "email": "emailchanged@example.com",
        }
        response = self.client.put(
            f"/api/professors/{self.professor.id}/", data=professor_change_data
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data.get("success"), "Professor alterado com sucesso")

    def test_delete_professor(self):
        response = self.client.delete(f"/api/professors/{self.professor.id}/")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data.get("success"), "Professor removido com sucesso")


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

        self.student = StudentRepository().save(
            {
                "name": "Test Student",
                "email": "studenttest@example.com",
                "password": "1234",
                "birth_date": "2000-01-01",
            }
        )

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
        self.assertEqual(response.data.get("success"), "Aluno cadastrado com sucesso")

    def test_put_student(self):
        student_change_data = {
            "email": "emailchanged@example.com",
        }
        response = self.client.put(
            f"/api/students/{self.student.id}/", data=student_change_data
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data.get("success"), "Aluno alterado com sucesso")

    def test_delete_student(self):
        response = self.client.delete(f"/api/students/{self.student.id}/")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data.get("success"), "Aluno removido com sucesso")
