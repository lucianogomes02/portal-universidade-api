from django.test import TestCase

from src.courses.repository.course_repository import CourseRepository
from src.grades.repository.grade_repository import GradeRepository
from src.grades.service.grade.serializers import GradeSerializer
from src.users.repository.professor_repository import ProfessorRepository
from src.users.repository.student_repository import StudentRepository


class GradesSerializerTestCase(TestCase):
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

        self.course = CourseRepository().save(
            {
                "name": "Course Test",
                "professor": self.professor,
                "workload": 100,
            }
        )

        self.grade_data = {
            "student": self.student.id,
            "professor": self.professor.id,
            "course": self.course.id,
            "value": 10.0,
        }

    def test_serializer_must_be_valid(self):
        serializer = GradeSerializer(data=self.grade_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_serializer_must_be_valid_on_update(self):
        grade_data = {
            "student": self.student,
            "professor": self.professor,
            "course": self.course,
            "value": 10.0,
        }
        grade = GradeRepository().save(grade_data=grade_data)
        updated_data = {"value": 8.75}
        serializer = GradeSerializer(instance=grade, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_serializer_must_not_be_valid_due_invalid_grade_value(self):
        invalid_data = {
            "student": self.student.id,
            "professor": self.professor.id,
            "course": self.course.id,
            "value": -10.0,
        }
        serializer = GradeSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("value", serializer.errors)
        self.assertEquals(
            serializer.errors.get("value")[0],
            "A Nota deve ser maior ou igual a 0 e decimal",
        )

    def test_serializer_must_not_be_valid_due_missing_student_field(self):
        invalid_data = {
            "professor": self.professor.id,
            "course": self.course.id,
            "value": 10.0,
        }
        serializer = GradeSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("student", serializer.errors)
