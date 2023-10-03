from typing import Dict
from uuid import UUID

from django.contrib.auth.models import Group
from django.db.models import QuerySet

from src.libs.repository import Repository
from src.users.models import Coordinator, User


class CoordinatorRepository(Repository):
    def __init__(self):
        self.coordinator_user = Coordinator

    def search_all_objects(self) -> QuerySet[Coordinator]:
        return self.coordinator_user.objects.all()

    def search_by_id(self, coordinator_id: UUID) -> Coordinator:
        return self.coordinator_user.objects.filter(id=coordinator_id).first()

    def save(self, coordinator_data: Dict) -> Coordinator:
        coordinator_json = {**coordinator_data}
        coordinator = Coordinator.objects.create(
            **coordinator_data,
            username=coordinator_json.get("email"),
            user_type=User.UserType.COORDINATOR
        )
        coordinator.set_password(coordinator.password)
        coordinator_group = Group.objects.filter(name="CoordinatorGroup").first()
        coordinator.groups.add(coordinator_group)
        coordinator.save()
        return coordinator

    def update(self, coordinator: Coordinator, updated_data: Dict) -> Coordinator:
        for key, value in updated_data.items():
            if hasattr(coordinator, key) and getattr(coordinator, key) != value:
                setattr(coordinator, key, value)

        new_password = updated_data.get("password")
        if new_password:
            coordinator.set_password(new_password)

        coordinator.save()
        return coordinator

    def delete(self, coordinator: Coordinator):
        coordinator.delete()
