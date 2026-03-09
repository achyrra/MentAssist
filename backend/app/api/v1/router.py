from fastapi import APIRouter
from app.clients.router import router as clients_router
from app.appointments.router import router as appointments_router
from app.users.router import router as users_router

router = APIRouter()
router.include_router(clients_router, prefix="/clients", tags=["clients"])
router.include_router(appointments_router, prefix="/appointments", tags=["appointments"])
router.include_router(users_router, prefix="/users", tags=["users"])