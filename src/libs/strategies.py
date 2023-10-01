import abc
from uuid import UUID

from django.db.models import QuerySet


class EntityFilterBasedOnUserTypeStrategy(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def filter_entity_based_user_type(entity_id: UUID, queryset: QuerySet):
        raise NotImplementedError()
