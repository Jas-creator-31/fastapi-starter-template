import pytest
from httpx import ASGITransport, AsyncClient

from settings import self_url
from src.main import app


@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=self_url) as ac:
        yield ac
