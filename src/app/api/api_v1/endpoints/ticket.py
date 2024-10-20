from fastapi import APIRouter

router = APIRouter(
    prefix="/ticket",
    tags=["Ticket"],
)


@router.get("/")
def get():
    ...

