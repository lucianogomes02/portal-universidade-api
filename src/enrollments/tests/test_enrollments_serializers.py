from django.test import TestCase

from src.courses.repository.course_repository import CourseRepository
from src.enrollments.service.serializers import EnrollmentSerializer
from src.users.repository.professor_repository import ProfessorRepository
from src.users.repository.student_repository import StudentRepository


class EnrollmentSerializerTestCase(TestCase):
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

        self.enrollment_data = {"student": self.student.id, "course": self.course.id}

    def test_serializer_must_be_valid(self):
        serializer = EnrollmentSerializer(data=self.enrollment_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_serializer_must_not_be_valid_due_invalid_student_field(self):
        invalid_data = {"student": self.student, "course": self.course.id}
        serializer = EnrollmentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("student", serializer.errors)
        self.assertEquals(
            serializer.errors.get("student")[0],
            "“studenttest@example.com” is not a valid UUID.",
        )

    def test_serializer_must_not_be_valid_due_missing_course_field(self):
        invalid_data = {"student": self.student.id}
        serializer = EnrollmentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("course", serializer.errors)
