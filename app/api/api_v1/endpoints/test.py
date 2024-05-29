from fastapi import APIRouter

router = APIRouter(
    prefix="/test",
    tags=["Test"],
)


@router.get("/")
def get():
    return "Hello World"
