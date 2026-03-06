from fastapi import APIRouter
from clients.router import router as clients_router
from appointments.router import router as appointments_router

router = APIRouter()
router.include_router(clients_router, prefix="/clients", tags=["clients"])
router.include_router(appointments_router, prefix="/appointments", tags=["appointments"])