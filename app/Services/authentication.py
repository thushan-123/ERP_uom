from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from ninja.security import HttpBearer

from app.Schemas import LoginSchema


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

def login_user(request, payload: LoginSchema):
    user = authenticate(request,username=payload.username, password=payload.password)
    token , _ = Token.objects.get_or_create(user=user)
    return {
        "token": token.key,
        "token_type": "Bearer",
    }