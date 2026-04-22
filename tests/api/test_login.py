from tests.api.async_client import async_client  # noqa: F401
import pytest

@pytest.mark.asyncio
async def test_login_success(async_client):  # noqa: F811
    payload = {
        "email": "jas123hanpreet@gmail.com",
        "password": "root_123"
    }
    res = await async_client.post("auth/login", json=payload)
    assert res.status_code == 200
