from rest_framework import permissions
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate

from core.responses import SuccessResponse, ErrorResponse
from ..serializers import CreateUserSerializer
from ..utils import get_tokens_for_user

User = get_user_model()


class LoginView(APIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            target_user = authenticate(email=email, password=password)
            tokens = get_tokens_for_user(target_user)

            return SuccessResponse(tokens)
        except Exception as e:
            return ErrorResponse(message='Invalid credentials')
