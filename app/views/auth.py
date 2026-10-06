from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from ninja import NinjaAPI, Router
from app.Services import login_user
from app.Schemas import TokenResponseSchema, LoginSchema

router = Router(tags=["authentication"])

@router.post("/login", auth=None, response=TokenResponseSchema)
def login(request, payload: LoginSchema):
    return login_user(request, payload)
