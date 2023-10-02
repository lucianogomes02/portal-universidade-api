from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.courses.repository.course_repository import CourseRepository
from src.enrollments.repository.enrollment_repository import EnrollmentRepository
from src.users.models import User
from src.users.repository.professor_repository import ProfessorRepository
from src.users.repository.student_repository import StudentRepository


class EnrollmentsAPITestCase(APITestCase):
    def setUp(self):
        self.enrollments_list = reverse("Enrollments-list")
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

        self.student = StudentRepository().save(
            {
                "name": "Test Student",
                "email": "studenttest@example.com",
                "password": "1234",
                "birth_date": "2000-01-01",
            }
        )

        self.enrollment_data = {
            "student": self.student,
            "course": self.course,
        }

        self.enrollments = EnrollmentRepository().save(self.enrollment_data)

    def test_get_enrollments(self):
        response = self.client.get(self.enrollments_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_courses(self):
        enrollment_data = {
            "student": self.student.id,
            "course": self.course.id,
        }
        response = self.client.post(self.enrollments_list, data=enrollment_data)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data.get("error"),
            f"Aluno {self.student.name} já está matrículado à Disciplina {self.course.name}",
        )
