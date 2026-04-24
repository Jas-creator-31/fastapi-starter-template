import pytest
from httpx import ASGITransport, AsyncClient

from settings import settings
from src.main import app


@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=settings.self_url) as ac:
        yield ac
