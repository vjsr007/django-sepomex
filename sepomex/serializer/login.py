from rest_framework import serializers
from ..model.user import User

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "pass_field")