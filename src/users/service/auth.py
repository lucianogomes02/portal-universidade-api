import os

import jwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserTokenSerializer(TokenObtainPairSerializer):
    def validate(self, data):
        data = super().validate(data)
        token = self.get_token(self.user)

        jwt_payload = token.access_token.payload.copy()
        jwt_payload["user"] = {
            "id": str(jwt_payload["user_id"]),
            "username": self.user.name,
            "permissions": list(self.user.get_group_permissions()),
        }
        jwt_payload.pop("user_id")

        token = jwt.encode(
            jwt_payload,
            os.getenv("SECRET_KEY"),
            algorithm="HS256",
        )

        data["access"] = token

        return data


class LoginView(TokenObtainPairView):
    serializer_class = UserTokenSerializer
