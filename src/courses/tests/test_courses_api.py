from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.courses.repository.course_repository import CourseRepository
from src.users.models import User
from src.users.repository.professor_repository import ProfessorRepository


class CoursesAPITestCase(APITestCase):
    def setUp(self):
        self.courses_list = reverse("Courses-list")
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

        self.course = CourseRepository().save(
            {
                "name": "Course Test",
                "professor": self.professor,
                "workload": 100,
            }
        )

    def test_get_courses(self):
        response = self.client.get(self.courses_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_courses(self):
        course_data = {
            "name": "Course Test 2",
            "professor": self.professor.id,
            "workload": 50,
        }

        response = self.client.post(self.courses_list, data=course_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data.get("success"), "Disciplina cadastrada com sucesso"
        )

    def test_put_course(self):
        course_change_data = {
            "name": "Teste Course Changed",
        }
        response = self.client.put(
            f"/api/courses/{self.course.id}/", data=course_change_data
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(
            response.data.get("success"), "Disciplina alterada com sucesso"
        )

    def test_delete_course(self):
        response = self.client.delete(f"/api/courses/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(
            response.data.get("success"), "Disciplina removida com sucesso"
        )
