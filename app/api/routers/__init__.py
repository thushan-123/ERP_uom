from ninja import Router

from .uom_master_router import router as uom_master_router

router = Router("/uom", uom_master_router , tags=["UOM Master"])