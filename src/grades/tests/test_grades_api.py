from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.courses.repository.course_repository import CourseRepository
from src.enrollments.repository.enrollment_repository import EnrollmentRepository
from src.grades.repository.grade_repository import GradeRepository
from src.users.models import User
from src.users.repository.professor_repository import ProfessorRepository
from src.users.repository.student_repository import StudentRepository


class GradesAPITestCase(APITestCase):
    def setUp(self):
        self.grades_list = reverse("Grades-list")
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

        self.enrollment = EnrollmentRepository().save(
            {"student": self.student, "course": self.course}
        )

        self.grade_data = {
            "student": self.student.id,
            "professor": self.professor.id,
            "course": self.course.id,
            "value": 10.0,
        }

    def test_get_grades(self):
        response = self.client.get(self.grades_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_grades(self):
        response = self.client.post(self.grades_list, data=self.grade_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("success"), "Nota regsitrada com sucesso")

    def test_put_course(self):
        self.client.post(self.grades_list, data=self.grade_data)

        grade = GradeRepository().search_by_student(student_id=self.student.id)

        course_change_data = {
            "student": self.student.id,
            "value": 8.5,
        }
        response = self.client.put(f"/api/grades/{grade.id}/", data=course_change_data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data.get("success"), "Nota foi alterada com sucesso")
