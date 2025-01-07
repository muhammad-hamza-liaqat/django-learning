from rest_framework import serializers
import re

from rest_framework import serializers
from custom_auth.models import User
import re

class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use!")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")

        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character")

        return value


class LoginSerializer(serializers.Serializer):
    email= serializers.EmailField()
    password = serializers.CharField()

    