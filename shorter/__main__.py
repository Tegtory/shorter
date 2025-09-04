import asyncio
import logging
import os
import sys

from shorter.presentors.aiogram.main import main as aiogram_service
from shorter.presentors.fastapi.main import main as fastapi_service


async def main(argv: list[str]) -> None:
    fastapi = asyncio.create_task(fastapi_service())
    aiogram = asyncio.create_task(aiogram_service(os.environ.get("BOT_TOKEN")))

    await asyncio.gather(aiogram, fastapi)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    asyncio.run(main(sys.argv))
