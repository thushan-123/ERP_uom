from django.db import transaction, IntegrityError
from ninja.errors import HttpError
from rest_framework import status
from app.models import UOMMaster
from app.schemas import UOMMasterCreate, UOMMasterUpdate
from django.shortcuts import get_object_or_404

def UOMMasterCreateService(request, payload: UOMMasterCreate):
    data = payload.model_dump()

    try:
        with transaction.atomic():
            uom = UOMMaster.objects.create(**data, created_by=request.auth, modified_by=request.auth,)
        return 201, {
            "success": True,
            "message": "UOM created successfully",
            "data": uom,
        }
    except IntegrityError:
        raise HttpError(400, "Already Exists")



def UOMMasterUpdateService(request, uom_id: int , payload: UOMMasterUpdate):
    uom = UOMMaster.objects.get(uom_id=uom_id)
    if uom is None:
        raise HttpError(404, "UOM not found")

    data = payload.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(uom, field, value)

    uom.modified_by = request.auth

    try:
        with transaction.atomic():
            uom.save()
            return 200, {
                "success": True,
                "message": "UOM updated successfully",
                "data": uom,
            }
    except IntegrityError:
        raise HttpError(400, "Update error")



def UOMMasterDiactivateService(request, uom_id: int):
    uom = get_object_or_404(UOMMaster, uom_id=uom_id)

    uom.active = not uom.active
    uom.modified_by = request.auth

    uom.save(
        update_fields=[
            "active",
            "modified_by",
            "modified_at",
        ]
    )

    return 200, {
        "success": True,
        "message": "UOM deactivated successfully",
        "data": uom,
    }

def UOMMasterGetAllService(request):
    uom_list = UOMMaster.objects.all()

    return 200, {
        "success": True,
        "message": "UOM list retrieved successfully",
        "data": uom_list,
    }

