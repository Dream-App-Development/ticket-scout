import json
from fastapi import APIRouter

router = APIRouter(
    prefix="/station",
    tags=["Station"],
)


@router.get("/")
def get_stations():
    ...

