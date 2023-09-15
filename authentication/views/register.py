from django.conf import settings
from rest_framework import permissions
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.validators import ValidationError

from core.responses import SuccessResponse, ErrorResponse
from core.threads import send_mail
from ..serializers import CreateUserSerializer
from ..mixins import TokenGeneratorMixin

User = get_user_model()


class SimpleRegistrationView(TokenGeneratorMixin, APIView):
    """Register and login api instant """

    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        # user registration
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        except ValidationError as error:
            return ErrorResponse(error=error.detail, message='Validation Error')
        except Exception as e:
            return ErrorResponse(exception=str(e))

        # generate user token
        try:
            token = self.make_token(user=user)
        except Exception:
            user.delete()
            return ErrorResponse(message='Something went wrong in generating user token')

        # send activation email
        try:
            subject = 'Email Confirmation'
            template = 'register.html'
            context = {'user': user, 'token': token,
                       'page_url': f"{settings.APP_UTILS['APP_URL']}/verify-email"}
            recipient_list = [user.email]

            send_mail(subject=subject, html_content=template,
                      key=context, recipient_list=recipient_list)
        except Exception as e:
            user.delete()
            return ErrorResponse(exception=e)

        return SuccessResponse(message='Activation email has been sent successfully')
