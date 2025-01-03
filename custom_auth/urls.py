from django.urls import path
from custom_auth.views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]