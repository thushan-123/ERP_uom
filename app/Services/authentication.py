from rest_framework.authtoken.models import Token
from ninja.security import HttpBearer


class BearerTokenAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            token_obj = Token.objects.select_related("user").get(
                key=token
            )
        except Token.DoesNotExist:
            return None

        if not token_obj.user.is_active:
            return None

        return token_obj.user