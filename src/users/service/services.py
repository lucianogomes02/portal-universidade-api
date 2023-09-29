from src.users.domain.entities import Coordinator
from src.users.models import CoordinatorUser, User


class CoordinatorService:
    @staticmethod
    def register_coordinator(name, email, password, birth_date) -> CoordinatorUser:
        coordinator = Coordinator(
            name=name, email=email, password=password, birth_date=birth_date
        )
        # validade coordinator here
        coordinator_user = CoordinatorUser.objects.create(
            name=name,
            email=email,
            birth_date=birth_date,
            username=coordinator.email,
            user_type=User.UserType.COORDINATOR,
        )
        coordinator_user.set_password(password)
        coordinator_user.save()
        return coordinator_user
