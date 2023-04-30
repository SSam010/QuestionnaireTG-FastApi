from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from clients.router import get_all_clients

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/clients")
def get_pages_with_all_clients(request: Request, clients=Depends(get_all_clients)):
    return templates.TemplateResponse("clients.html", {"request": request, "clients": clients["data"]})

