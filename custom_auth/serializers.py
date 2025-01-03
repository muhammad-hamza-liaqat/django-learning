from rest_framework import serializers
import re

class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        from .models import User
        try:
            User.get_user_by_email(value)
            raise serializers.ValidationError("Email already in use!")
        except Exception:
            return value
        
    def validate_password(self, value):
        if len(value)<3:
            raise serializers.ValidationError("Password must be at least 3 characters long")
        
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")


class LoginSerializer(serializers.Serializer):
    email= serializers.EmailField()
    password = serializers.CharField(write_only=True)

    