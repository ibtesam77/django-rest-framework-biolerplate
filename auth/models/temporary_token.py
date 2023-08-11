from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.conf import settings


class TemporaryToken(Token):
    """Subclass of Token to add an expiration time."""
    expiry_time = models.DateTimeField(default=timezone.now()
                                       + timezone.timedelta(
        minutes=settings.REST_FRAMEWORK_TEMPORARY_TOKENS['MINUTES'])
    )

    # class Meta(object):
    #     app_label = 'rest_framework_temporary_tokens'

    @property
    def is_expired(self):
        """Returns a boolean indicating token expiration."""
        return self.expiry_time <= timezone.now()

    def expire(self):
        """Expires a token by setting its expiration date to now."""
        self.expiry_time = timezone.now()
        self.save()
