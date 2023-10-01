from rest_framework import serializers


class UserPermissionsSerializer(serializers.Serializer):
    permissions = serializers.ListField(child=serializers.CharField())
