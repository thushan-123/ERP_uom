from ninja import Router

from app.schemas import UOMMasterCreate, UOMMasterUpdate,UOMResponse,UOMResponseList
from app.schemas import MessageSchema
from app.service import UOMMasterCreateService, UOMMasterDiactivateService,UOMMasterUpdateService,UOMMasterGetAllService, BearerTokenAuth

router = Router(auth=BearerTokenAuth() ,tags=["uom_master"])


@router.get("/test")
def test_uom(request):
    return {"message": "UOM API working"}

@router.post("" , response={201: UOMResponse, 409: MessageSchema})
def create(request, payload: UOMMasterCreate):
    return UOMMasterCreateService(request, payload)

@router.get("", response={200: UOMResponseList})
def get(request):
    return UOMMasterGetAllService(request)

@router.put("/{uom_id}" , response={200: UOMResponse, 409: MessageSchema})
def update(request,uom_id:int , payload: UOMMasterUpdate):
    return UOMMasterUpdateService(request,uom_id,payload)

@router.patch("/{uom_id}", response={200: UOMResponse, 409: MessageSchema})
def patch(request, uom_id: int):
    return UOMMasterDiactivateService(request, uom_id)