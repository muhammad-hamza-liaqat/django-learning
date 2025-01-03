from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from custom_auth.serializers import SignUpSerializer
from custom_auth.models import User
from rest_framework import status



class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        if User.objects.filter(email=validated_data["email"]).exists():
            raise ValidationError({"email": "Email already in use!"})
        
        print("hashing the password")
        hashed_password = make_password(validated_data["password"])
        print(f"password hased", hashed_password)

        user = User.objects.create(
            name=validated_data["name"],
            email=validated_data["email"],
            password=hashed_password,
        )

        return Response({
            "message": "User registered successfully",
            "user_id": str(user.id),
        }, status=status.HTTP_201_CREATED)
