from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

from ..models import TemporaryToken

User = get_user_model()


class TemporaryTokenMixin():
    def get_temporary_token(self, user=None, *args, **kwargs):
        try:
            User.objects.get(email=user.email)
        except Exception as e:
            raise e

        try:
            token, _ = TemporaryToken.objects.get_or_create(user=user)

            if token and token.is_expired:
                # If the token is expired, generate a new one.
                token.delete()
                expiry_time = timezone.now() + timezone.timedelta(
                    minutes=settings.REST_FRAMEWORK_TEMPORARY_TOKENS['MINUTES'])

                token = TemporaryToken.objects.create(
                    user=user, expiry_time=expiry_time)

            return token.key
        except Exception as e:
            raise e

    def authenticate_temporary_token(self, token=None, *args, **kwargs):
        try:
            target_temp_token = TemporaryToken.objects.get(key=token)
            target_user = target_temp_token.user

            # delete temporary token after authentication
            target_temp_token.delete()

            return target_user
        except Exception as e:
            raise e
