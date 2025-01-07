from rest_framework import serializers
import re
from django.contrib.auth.models import User


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already in use!")
        if len(value) < 4:
            raise serializers.ValidationError("Username must be at least 4 characters long")
        if not value.isalnum():
            raise serializers.ValidationError("Username must be alphanumeric")
        return value

    def validate_first_name(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("First name cannot be empty")
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only alphabetic characters")
        return value

    def validate_last_name(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Last name cannot be empty")
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only alphabetic characters")
        return value

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

    