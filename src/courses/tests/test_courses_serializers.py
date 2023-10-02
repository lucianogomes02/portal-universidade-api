from django.test import TestCase

from src.courses.repository.course_repository import CourseRepository
from src.courses.service.course.serializers import CourseSerializer
from src.users.repository.professor_repository import ProfessorRepository
from src.users.repository.student_repository import StudentRepository


class CoursesSerializerTestCase(TestCase):
    def setUp(self):
        self.professor = ProfessorRepository().save(
            {
                "name": "Test Professor",
                "email": "professortest@example.com",
                "password": "1234",
                "birth_date": "2000-01-01",
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

        self.course_data = {
            "name": "Course Test",
            "professor": self.professor.id,
            "students": [self.student.id],
            "workload": 100,
        }

        self.course = CourseRepository().save(
            {
                "name": "Course Test",
                "professor": self.professor,
                "students": [self.student],
                "workload": 100,
            }
        )

    def test_serializer_must_be_valid(self):
        serializer = CourseSerializer(data=self.course_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_serializer_must_be_valid_on_update(self):
        updated_data = {"name": "Updated Course Name"}
        serializer = CourseSerializer(
            instance=self.course, data=updated_data, partial=True
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_serializer_must_not_be_valid_due_invalid_workload_field(self):
        invalid_data = {
            "name": "Course Test",
            "professor": self.professor.id,
            "students": [self.student.id],
            "workload": -10,
        }
        serializer = CourseSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("workload", serializer.errors)
        self.assertEquals(
            serializer.errors.get("workload")[0],
            "A carga horária deve ser um número inteiro maior que zero.",
        )

    def test_serializer_must_not_be_valid_due_missing_professor_field(self):
        invalid_data = {
            "name": "Course Test",
            "students": [self.student.id],
            "workload": 100,
        }
        serializer = CourseSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("professor", serializer.errors)
