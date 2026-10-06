from ninja import Router

from app.Schemas import UOMResponseSchema, UOMCreateSchema, UOMUpdateSchema
from app.Schemas import MessageSchema
from app.Services import create_uom, update_uom, deactivate_uom, get_uom, BearerTokenAuth

router = Router(auth=BearerTokenAuth() ,tags=["uom_master"])

@router.get("/test")
def test_uom(request):
    return {"message": "UOM API working"}

@router.post("" , response={201: UOMResponseSchema, 409: MessageSchema})
def create(request, payload: UOMCreateSchema):
    return create_uom(request, payload)

@router.get("" , response=list[UOMResponseSchema])
def get(request):

    return get_uom(request)

@router.put("/{uom_id}" , response=UOMResponseSchema)
def update(request,uom_id:int , payload: UOMUpdateSchema):
    return update_uom(request,uom_id,payload)

@router.patch("/{uom_id}", response=UOMResponseSchema)
def patch(request, uom_id: int):
    return deactivate_uom(request, uom_id)