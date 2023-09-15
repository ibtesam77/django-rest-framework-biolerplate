from django.contrib.auth import get_user_model
from rest_framework import permissions, permissions
from rest_framework.views import APIView

from core.responses import SuccessResponse, ErrorResponse
from ..serializers import VerifyEmailSerializer
from ..mixins import TokenGeneratorMixin

User = get_user_model()


class VerifyEmailView(TokenGeneratorMixin, APIView):
    """Verify email api instant """
    serializer_class = VerifyEmailSerializer
    permission_classes = (permissions.AllowAny,)

    def patch(self, request, *args, **kwargs):
        # validate payload
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
        except Exception:
            return ErrorResponse(error=serializer.errors, message='Invalid payload')

        uid = request.data.get('uid', None)
        token = request.data.get('token', None)

        # validate user
        try:
            target_user = User.objects.get(id=uid)
        except Exception:
            return ErrorResponse(message='User not found against provided payload')

        try:
            self.check_token(user=target_user, token=token)
        except Exception:
            return ErrorResponse(message='Invalid or expired token')

        try:
            target_user.is_active = True
            target_user.save()
        except Exception:
            return ErrorResponse(message='Something went wrong in activating email')

        return SuccessResponse(message='Email activated successfully')
