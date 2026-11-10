"""
URL configuration for erp project.

The `urlpatterns` list routes URLs to api. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function api
    1. Add an import:  from my_app import api
    2. Add a URL to urlpatterns:  path('', api.home, name='home')
Class-based api
    1. Add an import:  from other_app.api import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.urls import path
from ninja import NinjaAPI

from app.api import router as uom_router
from app.api import auth_router
from app.schemas import UOMErrorMessageSchema

api = NinjaAPI(
    title="UOM Management API",
    version="1.0.0",
)
@api.exception_handler(UOMErrorMessageSchema)
def uom_error_handler(request, exc: UOMErrorMessageSchema):
    return JsonResponse(
        exc.send(),
        status=exc.code,
    )

# Auto-create default user
def ensure_default_user():
    User = get_user_model()
    if not User.objects.filter(username="abc").exists():
        User.objects.create_user(username="abc", password="123456")

try:
    ensure_default_user()
except Exception:
    pass

api.add_router("/uom", uom_router)
api.add_router("/auth", auth_router)

urlpatterns = [
    path("api/", api.urls),
]