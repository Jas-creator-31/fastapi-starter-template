from src.core.logging.logging import setup_logging
from fastapi import FastAPI
from src.core.application.lifespan import lifespan
from src.core.errors.exc_handler import exception_handler
from src.core.middleware.register_middleware import register_middleware
from src.core.rate_limiting.limiter import limiter
from src.features.auth.routes.auth import auth_router
from src.db.session import radar_engine
from fastapi_radar import Radar
import logging

setup_logging()

app = FastAPI(
    lifespan=lifespan, # type: ignore
    debug=True,
)
radar = Radar(app=app, db_engine=radar_engine, storage_engine=radar_engine)  # type: ignore

app.state.radar = radar
app.state.limiter = limiter

register_middleware(app)
exception_handler(app)
app.include_router(auth_router)

logger = logging.getLogger(__name__)

@app.get("/")
@limiter.exempt
async def health_check() -> dict[str, str]:
    logger.info("health check successful")
    return {"status": "ok"}
