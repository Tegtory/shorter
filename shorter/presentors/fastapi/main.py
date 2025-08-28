import logging

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from shorter.common.config import config
from shorter.infrastructure.di import container

from .handlers import router

logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Starting FastAPI server")
    app = FastAPI()
    app.include_router(router)
    setup_dishka(container, app)
    host = "0.0.0.0" if not config.DEBUG else "127.0.0.1"
    server_config = uvicorn.Config(app, host=host, port=9123)
    server = uvicorn.Server(server_config)
    logger.info("FastAPI serving %s:%s", host, 9123)
    await server.serve()
