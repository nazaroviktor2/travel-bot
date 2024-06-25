from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapp.api.v1 import router as api_v1
from webapp.metrics import metrics
from webapp.middleware.logger import LogServerMiddleware
from webapp.on_startup.logger import setup_logger
from webapp.on_startup.redis import start_redis


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(
        LogServerMiddleware,
    )

    # CORS Middleware should be the last.
    # See https://github.com/tiangolo/fastapi/issues/1663 .
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_routers(app: FastAPI) -> None:
    app.add_route("/metrics", metrics)

    app.include_router(router=api_v1.router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_logger()

    await start_redis()

    print("START APP")
    yield
    print("END APP")


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    setup_middleware(app)
    setup_routers(app)

    return app
