from django.contrib.auth import authenticate
from ninja.errors import HttpError
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


def login_user(request, payload):
    user = authenticate(
        request=request,
        username=payload.username,
        password=payload.password,
    )

    if user is None:
        raise HttpError(401, "Invalid username or password")

    if not user.is_active:
        raise HttpError(403, "User account is inactive")

    token, _ = Token.objects.get_or_create(user=user)

    return {
        "access_token": token.key,
        "token_type": "Bearer",
    }