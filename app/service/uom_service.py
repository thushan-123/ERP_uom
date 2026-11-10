from django.db import transaction, IntegrityError
from ninja.errors import HttpError
from rest_framework import status
from app.models import UOMMaster
from app.schemas import UOMMasterCreate, UOMMasterUpdate, UOMErrorMessageSchema
from django.shortcuts import get_object_or_404

def UOMMasterCreateService(request, payload: UOMMasterCreate):
    data = payload.model_dump()

    try:
        with transaction.atomic():
            uom = UOMMaster.objects.create(**data ,created_by=request.auth, modified_by=request.auth,)  # created_by=request.auth, modified_by=request.auth,
        return 201, {
            "success": True,
            "message": "UOM created successfully",
            "data": uom,
        }
    except Exception as e:
        # raise HttpError(400, "UOM - Already Exists")
        raise UOMErrorMessageSchema("error",404,"Intergrity Error", "Uom Creation Error")

def UOMMasterUpdateService(request, uom_id: int , payload: UOMMasterUpdate):
    try:
        uom = UOMMaster.objects.filter(uom_id=uom_id).first()
        if uom is None:
            raise HttpError(404, "UOM not found")

        data = payload.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(uom, field, value)

        uom.modified_by = request.auth

        with transaction.atomic():
            uom.save()
            return 200, {
                "success": True,
                "message": "UOM updated successfully",
                "data": uom,
            }
    except Exception as e:
        # raise HttpError(400, "UOM Master Update Error")
        raise UOMErrorMessageSchema("error", 404, "Update Error", "Uom Creation Error")



def UOMMasterDiactivateService(request, uom_id: int):
    try:
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
    except Exception as e:
        # raise HttpError(400, "UOM Master Deactivate Error")
        raise UOMErrorMessageSchema("error", 404, "Deactivate Error", "Uom Creation Error")


def UOMMasterGetAllService(request):
    try:
        uom_list = UOMMaster.objects.all().order_by("uom_id")

        return 200, {
            "success": True,
            "message": "UOM list retrieved successfully",
            "data": uom_list,
        }
    except Exception as e:
        # raise HttpError(400, "UOM Master List Error")
        raise UOMErrorMessageSchema("error", 404, "List Error", "Uom Master List Error")

def UOMMasterDeleteService(request, uom_id: int):
    try:
        data = UOMMaster.objects.filter(uom_id=uom_id)
        if data is None:
            raise HttpError(404, "UOM Is Not Found")
        else:
            data.delete()
        return 200, {
            "success": True,
            "message": "UOM deleted successfully",
        }
    except Exception as e:
        # raise HttpError(400, "UOM Master Delete Service Error")
        raise UOMErrorMessageSchema("error", 404, "Delete Error", "Delete Error - UOMMasterDeleteService error")