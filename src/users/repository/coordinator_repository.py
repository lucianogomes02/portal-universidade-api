import abc
from typing import Dict
from uuid import UUID

from django.db.models import QuerySet

from src.users.models import CoordinatorUser, User


class Repository(abc.ABC):
    @abc.abstractmethod
    def search_all_objects(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def search_by_id(self, id):
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, id):
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, entity, updated_data):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, id):
        raise NotImplementedError()


class CoordinatorRepository(Repository):
    def __init__(self):
        self.coordinator_user = CoordinatorUser

    def search_all_objects(self) -> QuerySet[CoordinatorUser]:
        return self.coordinator_user.objects.all()

    def search_by_id(self, coordinator_id: UUID) -> CoordinatorUser:
        return self.coordinator_user.objects.filter(id=coordinator_id).first()

    def save(self, coordinator_data: Dict) -> CoordinatorUser:
        coordinator_json = {**coordinator_data}
        coordinator = CoordinatorUser.objects.create(
            **coordinator_data,
            username=coordinator_json.get("email"),
            user_type=User.UserType.COORDINATOR
        )
        coordinator.set_password(coordinator.password)
        coordinator.save()
        return coordinator

    def update(
        self, coordinator: CoordinatorUser, updated_data: Dict
    ) -> CoordinatorUser:
        for key, value in updated_data.items():
            if hasattr(coordinator, key) and getattr(coordinator, key) != value:
                setattr(coordinator, key, value)

        new_password = updated_data.get("password")
        if new_password:
            coordinator.set_password(new_password)

        coordinator.save()
        return coordinator

    def delete(self, coordinator: CoordinatorUser):
        coordinator.delete()
