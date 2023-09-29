from typing import Dict
from uuid import UUID

from django.db.models import QuerySet

from src.libs.repository import Repository
from src.users.models import Professor, User


class ProfessorRepository(Repository):
    def __init__(self):
        self.coordinator_user = Professor

    def search_all_objects(self) -> QuerySet[Professor]:
        return self.coordinator_user.objects.all()

    def search_by_id(self, coordinator_id: UUID) -> Professor:
        return self.coordinator_user.objects.filter(id=coordinator_id).first()

    def save(self, coordinator_data: Dict) -> Professor:
        coordinator_json = {**coordinator_data}
        coordinator = Professor.objects.create(
            **coordinator_data,
            username=coordinator_json.get("email"),
            user_type=User.UserType.PROFESSOR
        )
        coordinator.set_password(coordinator.password)
        coordinator.save()
        return coordinator

    def update(self, coordinator: Professor, updated_data: Dict) -> Professor:
        for key, value in updated_data.items():
            if hasattr(coordinator, key) and getattr(coordinator, key) != value:
                setattr(coordinator, key, value)

        new_password = updated_data.get("password")
        if new_password:
            coordinator.set_password(new_password)

        coordinator.save()
        return coordinator

    def delete(self, coordinator: Professor):
        coordinator.delete()
