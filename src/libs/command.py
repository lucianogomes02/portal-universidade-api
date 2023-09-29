import abc

from django.core.management import BaseCommand


class Command(abc.ABC, BaseCommand):
    @abc.abstractmethod
    def add_arguments(self, parser):
        raise NotImplementedError()

    @abc.abstractmethod
    def handle(self, *args, **options):
        raise NotImplementedError()
