from django.contrib.auth import authenticate
from  ninja import Schema

class LoginSchema(Schema):
    username :str
    password :str

class TokenResponseSchema(Schema):
    access_token :str
    token_type:str
