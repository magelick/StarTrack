from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from src.logger import logger
from src.settings import templating

router = APIRouter(prefix="")


@router.get(path="/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        return templating.TemplateResponse(
            "homepage.html", {"request": request}
        )
    except Exception as e:
        logger.error(e)


@router.get("/login", response_class=HTMLResponse)
async def login_template(request: Request):
    try:
        return templating.TemplateResponse("login.html", {"request": request})
    except Exception as e:
        logger.error(e)


@router.get(path="/parent_dashboard", response_class=HTMLResponse)
async def parent_dashboard_template(request: Request):
    try:
        return templating.TemplateResponse(
            "dashboard.html", {"request": request}
        )
    except Exception as e:
        logger.error(e)


@router.get(path="/ai_testing", response_class=HTMLResponse)
async def read_ai(request: Request):
    try:
        return templating.TemplateResponse(
            "ai_test.html", {"request": request}
        )
    except Exception as e:
        logger.error(e)
