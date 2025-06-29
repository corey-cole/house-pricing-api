import os
import shutil
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    generate_latest,
    multiprocess,
)
from prometheus_fastapi_instrumentator import Instrumentator

from .core.config import settings
from .v1 import router as v1_router


def setup_prometheus_multiproc_dir():
    """
    Set up the directory for Prometheus multiprocessing.

    This should be called on application startup. It ensures the directory
    exists and is clean. The prometheus-client library uses this directory
    to share metrics between processes.
    """
    prom_dir = os.environ.get("PROMETHEUS_MULTIPROC_DIR")
    if prom_dir:
        if os.path.exists(prom_dir):
            shutil.rmtree(prom_dir)
        os.makedirs(prom_dir, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager to handle startup/shutdown."""
    setup_prometheus_multiproc_dir()
    yield
    # No shutdown actions needed


app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


def metrics(request: Request) -> Response:
    """Custom metrics endpoint for multiprocessing."""
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)


Instrumentator().instrument(app)
app.add_route("/metrics", metrics)

app.include_router(v1_router.router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME}"}