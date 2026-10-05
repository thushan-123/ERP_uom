from django.db import transaction, IntegrityError
from ninja import Router, Schema
from ninja.errors import HttpError

from Models import uom_master
from Schemas import UOMCreateSchema, UOMUpdateSchema


def create_uom(request, payload: UOMCreateSchema):
    data = payload.model_dump()

    try:
        with transaction.atomic():
            uom = uom_master.objects.create(**data, created_by=request.auth, modified_by=request.auth,)

    except IntegrityError:
        raise HttpError(400, "Already Exists")

    return 201, uom

def update_uom(request, uom_id: int , payload: UOMUpdateSchema):
    uom = uom_master.objects.filter(id=uom_id)
    if uom is None:
        raise HttpError(404, "Not Found")
    data = payload.model_dump(exclude_unset=True)

    for field , value in data.items():
        setattr(uom, field, value)
    uom.modified_by = request.auth
    try:
        with transaction.atomic():
            uom.update()
    except IntegrityError:
        raise HttpError(400, "Update error")
    return uom

def deactivate_uom(request, uom_id: int ):
    uom = uom_master.objects.filter(id=uom_id).first()
    if uom is None:
        raise HttpError(404, "Not Found")

    if uom.active:
        uom.active = False
        uom.save(update_fields=["active", "modified_by", "modified_at"])
        return {"message": "UOM deactivated successfully"}
    else:
        uom.active = True
        uom.save(update_fields=["active", "modified_by", "modified_at"])
        return {"message": "UOM activated successfully"}

def get_uom(request ):
    uom_list = uom_master.objects.all()
    return uom_list

