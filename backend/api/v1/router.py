from fastapi import APIRouter
from clients.router import router as clients_router


router = APIRouter()
router.include_router(clients_router, prefix="/clients", tags=["clients"])
