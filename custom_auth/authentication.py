import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed("Access token is required")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        try:
            user = User.get_user_by_id(payload['user_id'])
        except Exception:
            raise AuthenticationFailed('User not found')

        if not user.isActive:
            raise AuthenticationFailed('User account is inactive')

        return (user, None)

    @staticmethod
    def generate_token(user):
        payload = {
            'user_id': user.id,
            'isActive': user.isActive,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
