import abc


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
