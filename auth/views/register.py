from rest_framework import permissions
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.validators import ValidationError
# from django.conf import settings

from core.responses import SuccessResponse, ErrorResponse
from ..serializers import CreateUserSerializer
from ..utils import get_tokens_for_user

User = get_user_model()
# email = settings.EMAIL_HOST_USER


class SimpleRegistrationView(APIView):
    """Register and login api instant """

    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                token = get_tokens_for_user(user)

                return SuccessResponse({
                    "user": self.serializer_class(user).data,
                    "token": token
                })
        except ValidationError as error:
            return ErrorResponse(error=error.detail, message='Validation Error')
        except Exception as e:
            return ErrorResponse(exception=str(e))
