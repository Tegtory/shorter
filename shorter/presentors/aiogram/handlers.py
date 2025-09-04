from typing import Any

from aiogram import F, Router, types
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from shorter.common.config import config
from shorter.domain import Link
from shorter.domain.use_cases import UCLink

from .messages import welcome

router = Router()


@router.message(F.text.startswith("/start"))
async def start(message: types.Message) -> Any:
    return await message.answer(welcome)


@router.message(F.text.startswith("https://"))
@inject
async def create_url(
    message: types.Message, use_case: FromDishka[UCLink]
) -> Any:
    try:
        link = await use_case.create(Link(link=message.text))
        await message.answer(f"Ссылка: {config.full_path()}/{link.uid}")
    except Exception:
        await message.answer("Произошла ошибка попробуйте позже")
