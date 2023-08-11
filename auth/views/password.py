from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import permissions, permissions
from rest_framework.views import APIView

from core.threads import send_mail
from core.responses import SuccessResponse, ErrorResponse
from ..serializers import ChangePasswordSerializer
from ..mixins import TokenGeneratorMixin

User = get_user_model()


class ForgotPasswordView(TokenGeneratorMixin, APIView):
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
        except User.DoesNotExist:
            error = {'detail': 'User with this email does not exist'}
            return ErrorResponse(error=error, message=error['detail'])

        try:
            token = self.make_token(user=target_user)
        except Exception:
            return ErrorResponse(message='Something went wrong in generating user token')

        # send email to user
        try:
            subject = 'Change Password'
            template = 'forgot_password.html'
            context = {'user': target_user, 'token': token,
                       'page_url': f"{settings.APP_UTILS['APP_URL']}/forgot-password"}
            recipient_list = [target_user.email]

            send_mail(subject=subject, html_content=template,
                      key=context, recipient_list=recipient_list)
        except Exception as e:
            return ErrorResponse(exception=e)

        return SuccessResponse(
            message='Email sent successfully to change your password')


class ChangePasswordView(TokenGeneratorMixin, APIView):
    """Change password api instant """
    serializer_class = ChangePasswordSerializer
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
        password = request.data.get('password', None)

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
            target_user.set_password(password)
            target_user.save()
        except Exception:
            return ErrorResponse(message='Something went wrong in updating user password')

        return SuccessResponse(message='Password changed successfully')
