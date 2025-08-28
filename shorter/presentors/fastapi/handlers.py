from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.responses import HTMLResponse

from shorter.common.exceptions import AppError
from shorter.domain import Link
from shorter.domain.use_cases.link import UCLink

router = APIRouter()


@router.post("/gen")
@inject
async def create_url(link: Link, use_case: FromDishka[UCLink]) -> dict:
    try:
        result = await use_case.create(link)
        return result.model_dump()
    except AppError as e:
        return {"error": e.message}


@router.get("/{uid}")
@inject
async def get_url(uid: str, use_case: FromDishka[UCLink]) -> HTMLResponse:
    url = use_case.get(uid)
    return HTMLResponse(
        f'<script>window.location.href="{url}"</script>', status_code=302
    )
