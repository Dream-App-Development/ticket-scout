import os

from fastapi import APIRouter

router = APIRouter(
    prefix="/test",
    tags=["Test"],
)


@router.get("/")
def get():
    return f"{os.getenv('APP_IDENT')} is working!"
