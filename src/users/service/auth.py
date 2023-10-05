import os

import jwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserTokenSerializer(TokenObtainPairSerializer):
    def validate(self, data):
        data = super().validate(data)
        self.get_token(self.user)

        data["user"] = {
            "id": str(self.user.id),
            "username": self.user.name,
            "permissions": list(self.user.get_group_permissions()),
        }

        return data


class LoginView(TokenObtainPairView):
    serializer_class = UserTokenSerializer
