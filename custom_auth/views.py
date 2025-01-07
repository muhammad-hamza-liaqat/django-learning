from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from custom_auth.serializers import SignUpSerializer, LoginSerializer
from django.contrib.auth.models import User
from rest_framework import status
from custom_auth.authentication import CustomJWTAuthentication

class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        hashed_password = make_password(validated_data["password"])

        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            password=hashed_password,
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"]
        )

        return Response({
            "message": "User registered successfully",
            "user_id": str(user.id),
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        email = validated_data["email"]
        password = validated_data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError({"detail": "Invalid email or password"})

        if not check_password(password, user.password):
            raise ValidationError({"detail": "Invalid email or password"})

        token = CustomJWTAuthentication.generate_token(user)
        return Response({
            "status": 200,
            "message": "Login successfully",
            "token": token
        }, status=status.HTTP_200_OK)
