import logging

from django.db import transaction, IntegrityError, DatabaseError
from django.db.models import ProtectedError, RestrictedError
from ninja.errors import HttpError

from app.models import UOMMaster
from app.schemas import UOMMasterCreate, UOMMasterUpdate

logger = logging.getLogger(__name__)


def _unexpected_error(action: str) -> HttpError:
    """Log the full traceback server-side, return a generic message to the client."""
    logger.exception("Unexpected error while %s", action)
    return HttpError(500, f"Unexpected error while {action}")


def _get_uom_or_404(uom_id: int, *, for_update: bool = False) -> UOMMaster:
    qs = UOMMaster.objects
    if for_update:
        qs = qs.select_for_update()  # must be called inside transaction.atomic()
    uom = qs.filter(uom_id=uom_id).first()
    if uom is None:
        raise HttpError(404, f"UOM with id {uom_id} not found")
    return uom


def UOMMasterCreateService(request, payload: UOMMasterCreate):
    data = payload.model_dump()

    try:
        with transaction.atomic():
            uom = UOMMaster.objects.create(
                **data,
                created_by=request.auth,
                modified_by=request.auth,
            )
    except IntegrityError:
        logger.warning("UOM create integrity error", exc_info=True)
        raise HttpError(409, "UOM already exists or violates a database constraint")
    except DatabaseError:
        raise _unexpected_error("creating UOM")
    except Exception:
        raise _unexpected_error("creating UOM")

    return 201, {
        "success": True,
        "message": "UOM created successfully",
        "data": uom,
    }


def UOMMasterUpdateService(request, uom_id: int, payload: UOMMasterUpdate):
    data = payload.model_dump(exclude_unset=True)

    try:
        with transaction.atomic():
            uom = _get_uom_or_404(uom_id, for_update=True)

            for field, value in data.items():
                setattr(uom, field, value)
            uom.modified_by = request.auth
            uom.save()
    except HttpError:
        raise  # keep the 404 (or any other deliberate HTTP error) intact
    except IntegrityError:
        logger.warning("UOM update integrity error (id=%s)", uom_id, exc_info=True)
        raise HttpError(409, "Update violates a database constraint (e.g. duplicate value)")
    except DatabaseError:
        raise _unexpected_error("updating UOM")
    except Exception:
        raise _unexpected_error("updating UOM")

    return 200, {
        "success": True,
        "message": "UOM updated successfully",
        "data": uom,
    }


def UOMMasterDiactivateService(request, uom_id: int):
    try:
        with transaction.atomic():
            uom = _get_uom_or_404(uom_id, for_update=True)

            uom.active = not uom.active
            uom.modified_by = request.auth
            uom.save(update_fields=["active", "modified_by", "modified_at"])
    except HttpError:
        raise
    except DatabaseError:
        raise _unexpected_error("toggling UOM status")
    except Exception:
        raise _unexpected_error("toggling UOM status")

    state = "activated" if uom.active else "deactivated"
    return 200, {
        "success": True,
        "message": f"UOM {state} successfully",
        "data": uom,
    }


def UOMMasterGetAllService(request):
    try:
        # Querysets are lazy; wrapping in list() forces evaluation inside the try block.
        uom_list = list(UOMMaster.objects.all().order_by("uom_id"))
    except DatabaseError:
        raise _unexpected_error("retrieving UOM list")
    except Exception:
        raise _unexpected_error("retrieving UOM list")

    return 200, {
        "success": True,
        "message": "UOM list retrieved successfully",
        "data": uom_list,
    }


def UOMMasterDeleteService(request, uom_id: int):
    try:
        with transaction.atomic():
            uom = _get_uom_or_404(uom_id, for_update=True)
            uom.delete()
    except HttpError:
        raise
    except (ProtectedError, RestrictedError):
        # Must come before IntegrityError (ProtectedError is a subclass of it)
        raise HttpError(409, "UOM is referenced by other records and cannot be deleted")
    except IntegrityError:
        logger.warning("UOM delete integrity error (id=%s)", uom_id, exc_info=True)
        raise HttpError(409, "UOM cannot be deleted due to a database constraint")
    except DatabaseError:
        raise _unexpected_error("deleting UOM")
    except Exception:
        raise _unexpected_error("deleting UOM")

    return 200, {
        "success": True,
        "message": "UOM deleted successfully",
    }