from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import permissions, permissions
from rest_framework.views import APIView
from rest_framework.validators import ValidationError

from core.threads import send_mail
from core.responses import SuccessResponse, ErrorResponse
from ..serializers import ChangePasswordSerializer
from ..mixins import TemporaryTokenMixin

User = get_user_model()


class ForgotPasswordView(TemporaryTokenMixin, APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email', '')

        # if no email is attached
        if email == '':
            error = {'detail': 'Email is required to reset password'}
            return ErrorResponse(error=error, message=error['detail'])

        # Create temporary token to reset password
        try:
            target_user = User.objects.get(email=email)
            token = self.get_temporary_token(user=target_user)

            # send email to user
            subject = 'Change Password'
            template = 'forgot_password.html'
            context = {'user': target_user, 'token': token,
                       'page_url': f"{settings.APP_UTILS['APP_URL']}/forgot-password"}
            recipient_list = [target_user.email]

            send_mail(subject=subject, html_content=template,
                      key=context, recipient_list=recipient_list)

            return SuccessResponse(
                message='Email sent successfully to change your password')
        except User.DoesNotExist:
            error = {'detail': 'User with this email does not exist'}
            return ErrorResponse(error=error, message=error['detail'])
        except Exception as e:
            return ErrorResponse(exception=e)


class ChangePasswordView(TemporaryTokenMixin, APIView):
    """Change password api instant """
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.AllowAny,)

    def patch(self, request, *args, **kwargs):
        # validate payload
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return ErrorResponse(error=str(e), message='Invalid payload')

        token = request.data.get('token', None)
        password = request.data.get('password', None)
        target_user = None

        # validate token
        try:
            target_user = self.authenticate_temporary_token(token=token)

            if target_user is None:
                raise ValidationError(
                    {'detail': 'No user found against target token'})

            target_user.set_password(password)
            target_user.save()

            return SuccessResponse(message='Password changed successfully')
        except Exception as e:
            return ErrorResponse(error=str(e), message='Invalid or expired token')
