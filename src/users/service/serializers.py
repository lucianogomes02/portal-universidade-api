from rest_framework import serializers

from src.users.models import CoordinatorUser


class CoordinatorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    birth_date = serializers.DateField(required=False)

    class Meta:
        model = CoordinatorUser
        fields = ["id", "name", "email", "password", "birth_date"]
