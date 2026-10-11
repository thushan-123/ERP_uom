from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from ninja import NinjaAPI, Router
from app.service import login_user
from app.schemas import TokenResponseSchema, LoginSchema

auth_router = Router(tags=["authentication"])

@auth_router.post("/login", auth=None, response=TokenResponseSchema)
def login(request, payload: LoginSchema):
    return login_user(request, payload)
