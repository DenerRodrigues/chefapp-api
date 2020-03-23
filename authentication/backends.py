from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from rest_framework_simplejwt.authentication import JWTAuthentication


User = get_user_model()


class CustomModelBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = str(username).strip().lower()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            email = None
        return super(CustomModelBackend, self).authenticate(request, email, password, **kwargs)


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        authentication = super(CustomJWTAuthentication, self).authenticate(request)
        return authentication
