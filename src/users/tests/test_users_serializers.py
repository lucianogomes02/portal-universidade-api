from django.test import TestCase
from src.users.models import Coordinator, User
from src.users.service.coordinator.serializers import CoordinatorSerializer
from src.users.service.professor.serializers import ProfessorSerializer
from src.users.service.student.serializers import StudentSerializer


class UsersSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            "name": "User Test",
            "email": "usertest@example.com",
            "password": "12345",
            "birth_date": "2000-01-01",
        }
        self.coordinator = User.objects.create(**self.user_data)

    def test_serializer_must_be_valid(self):
        serializer = CoordinatorSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

        serializer = ProfessorSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

        serializer = StudentSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_serializer_must_be_valid_on_update(self):
        updated_data = {"name": "Updated Coordinator Name"}
        serializer = CoordinatorSerializer(
            instance=self.coordinator, data=updated_data, partial=True
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

        updated_data = {"name": "Updated Professor Name"}
        serializer = ProfessorSerializer(
            instance=self.coordinator, data=updated_data, partial=True
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

        updated_data = {"name": "Updated Student Name"}
        serializer = StudentSerializer(
            instance=self.coordinator, data=updated_data, partial=True
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_serializer_must_not_be_valid_due_invalid_birth_date_field(self):
        invalid_data = {
            "name": "User Test",
            "email": "usertest@example.com",
            "password": "12345",
            "birth_date": "01/01/2000",
        }
        serializer = CoordinatorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("birth_date", serializer.errors)
        self.assertEquals(
            serializer.errors.get("birth_date")[0],
            "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
        )

        serializer = ProfessorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("birth_date", serializer.errors)
        self.assertEquals(
            serializer.errors.get("birth_date")[0],
            "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
        )

        serializer = StudentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("birth_date", serializer.errors)
        self.assertEquals(
            serializer.errors.get("birth_date")[0],
            "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
        )

    def test_serializer_must_not_be_valid_due_missing_email_field(self):
        invalid_data = {
            "name": "Coordinator Test",
            "password": "12345",
            "birth_date": "2000-01-01",
        }
        serializer = CoordinatorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

        serializer = ProfessorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

        serializer = StudentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
