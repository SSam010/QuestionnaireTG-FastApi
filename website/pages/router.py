from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from auth.base_config import current_superuser
from auth.models import User
from clients.router import get_all_clients, get_not_processed_clients

router = APIRouter(
    prefix="",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/clients")
def get_page_with_all_clients(request: Request,
                              clients=Depends(get_all_clients),
                              user: User = Depends(current_superuser)
                              ):
    return templates.TemplateResponse("clients.html", {"request": request,
                                                       "clients": clients["data"],
                                                       "page": clients["page"],
                                                       "down_page": clients["down_page"],
                                                       "has_more": clients["has_more"],
                                                       "max_page": clients["max_page"],
                                                       "user": user,
                                                       }
                                      )


@router.get("/clients/not_processed")
def get_page_not_processed_clients(request: Request,
                                   clients=Depends(get_not_processed_clients),
                                   user: User = Depends(current_superuser)
                                   ):
    return templates.TemplateResponse("clients.html", {"request": request,
                                                       "clients": clients["data"],
                                                       "page": clients["page"],
                                                       "down_page": clients["down_page"],
                                                       "has_more": clients["has_more"],
                                                       "max_page": clients["max_page"],
                                                       "user": user,
                                                       }
                                      )


@router.get("/auth")
def page_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/error403")
def get_page_error403(request: Request):
    return templates.TemplateResponse("error403.html", {"request": request})


@router.get("/error404")
def get_page_error404(request: Request):
    return templates.TemplateResponse("error404.html", {"request": request})


@router.get("/")
def get_page_start(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
