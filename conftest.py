from os import getenv

import pytest
from aiohttp import ClientSession
from dotenv import load_dotenv

assert load_dotenv()

BACKPACK_TF_TOKEN = getenv("BACKPACK_TF_TOKEN")
BACKPACK_TF_API_KEY = getenv("BACKPACK_TF_API_KEY")
STEAM_ID = getenv("STEAM_ID")
TRADE_URL = getenv("TRADE_URL")


@pytest.fixture
def backpack_tf_token() -> str:
    return BACKPACK_TF_TOKEN


@pytest.fixture
def backpack_tf_api_key() -> str:
    return BACKPACK_TF_API_KEY


@pytest.fixture
def steam_id() -> str:
    return STEAM_ID


@pytest.fixture
def trade_url() -> str:
    return TRADE_URL


@pytest.fixture
async def aiohttp_session():
    async with ClientSession() as session:
        yield session
