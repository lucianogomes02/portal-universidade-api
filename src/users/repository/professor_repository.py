from typing import Dict
from uuid import UUID

from django.db.models import QuerySet

from src.libs.repository import Repository
from src.users.models import Professor, User


class ProfessorRepository(Repository):
    def __init__(self):
        self.professor_user = Professor

    def search_all_objects(self) -> QuerySet[Professor]:
        return self.professor_user.objects.all()

    def search_by_id(self, professor_id: UUID) -> Professor:
        return self.professor_user.objects.filter(id=professor_id).first()

    def save(self, professor_data: Dict) -> Professor:
        professor_json = {**professor_data}
        professor = Professor.objects.create(
            **professor_data,
            username=professor_json.get("email"),
            user_type=User.UserType.PROFESSOR
        )
        professor.set_password(professor.password)
        professor.save()
        return professor

    def update(self, professor: Professor, updated_data: Dict) -> Professor:
        for key, value in updated_data.items():
            if hasattr(professor, key) and getattr(professor, key) != value:
                setattr(professor, key, value)

        new_password = updated_data.get("password")
        if new_password:
            professor.set_password(new_password)

        professor.save()
        return professor

    def delete(self, professor: Professor):
        professor.delete()
