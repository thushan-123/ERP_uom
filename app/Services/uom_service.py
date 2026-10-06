from django.db import transaction, IntegrityError
from ninja.errors import HttpError

from app.Models import uom_master
from app.Schemas import UOMCreateSchema, UOMUpdateSchema
from django.shortcuts import get_object_or_404

def create_uom(request, payload: UOMCreateSchema):
    data = payload.model_dump()

    try:
        with transaction.atomic():
            uom = uom_master.objects.create(**data, created_by=request.auth, modified_by=request.auth,)

    except IntegrityError:
        raise HttpError(400, "Already Exists")

    return 201, uom

def update_uom(request, uom_id: int , payload: UOMUpdateSchema):
    uom = uom_master.objects.get(uom_id=uom_id)
    if uom is None:
        raise HttpError(404, "UOM not found")

    data = payload.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(uom, field, value)

    uom.modified_by = request.auth

    try:
        with transaction.atomic():
            uom.save()
    except IntegrityError:
        raise HttpError(400, "Update error")

    return uom
    # if uom is None:
    #     raise HttpError(404, "Not Found")
    # data = payload.model_dump(exclude_unset=True)
    #
    # for field , value in data.items():
    #     setattr(uom, field, value)
    # uom.modified_by = request.auth
    # try:
    #     with transaction.atomic():
    #         uom.update()
    # except IntegrityError:
    #     raise HttpError(400, "Update error")
    # return uom

def deactivate_uom(request, uom_id: int):
    uom = get_object_or_404(uom_master, uom_id=uom_id)

    uom.active = not uom.active
    uom.modified_by = request.auth

    uom.save(
        update_fields=[
            "active",
            "modified_by",
            "modified_at",
        ]
    )

    return uom
def get_uom(request ):
    uom_list = uom_master.objects.all()
    return uom_list

