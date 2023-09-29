import uuid
from datetime import date

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("birth_date", date(2000, 1, 1))

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class UserType(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        PROFESSOR = "PROFESSOR", "Professor"
        COORDINATOR = "COORDINATOR", "Coordinator"

    user_type = models.CharField(
        _("UserType"),
        max_length=50,
        choices=UserType.choices,
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, unique=True)
    birth_date = models.DateField(blank=True)

    groups = models.ManyToManyField(Group, blank=True, related_name="User_set")
    user_permissions = models.ManyToManyField(
        Permission, blank=True, related_name="User_set"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


class CoordinatorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(user_type=User.UserType.COORDINATOR)
        )


class Coordinator(User):
    objects = CoordinatorManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user_type = User.UserType.COORDINATOR
        self.set_password(self.password)
        return super().save(*args, **kwargs)


class ProfessorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(user_type=User.UserType.PROFESSOR)
        )


class Professor(User):
    objects = CoordinatorManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user_type = User.UserType.PROFESSOR
        self.set_password(self.password)
        return super().save(*args, **kwargs)
