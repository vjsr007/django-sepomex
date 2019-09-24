from rest_framework import serializers
from ..model.user import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "photo", "active", "fullname")