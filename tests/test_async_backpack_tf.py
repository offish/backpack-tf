import pytest
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientResponseError

from src.backpack_tf import (
    AsyncBackpackTF,
    Listing,
    NeedsAPIKey,
    __title__,
    __version__,
)

user_agent = f"Listing goin' up! | {__title__} v{__version__}"
listing_id = None


async def test_user_agent(
    aiohttp_session: ClientSession, backpack_tf_token: str, steam_id: str
) -> None:
    bptf = AsyncBackpackTF(aiohttp_session, backpack_tf_token, steam_id)
    data = await bptf.register_user_agent()

    assert data["status"] == "active"
    assert data["client"] == user_agent
    assert data["current_time"] > 0
    assert data["expire_at"] > 0


async def test_create_listing(
    aiohttp_session: ClientSession, backpack_tf_token: str, steam_id: str
) -> None:
    global listing_id

    bptf = AsyncBackpackTF(aiohttp_session, backpack_tf_token, steam_id)
    sku = "263;6"
    intent = "buy"
    currencies = {"keys": 0, "metal": 0.11}
    details = "my test description"
    listing = await bptf.create_listing(sku, intent, currencies, details)

    assert isinstance(listing, Listing)
    assert isinstance(listing.item, dict)
    assert isinstance(listing.currencies, dict)
    assert listing.steamid == steam_id
    assert listing.intent == "buy"
    assert listing.appid == 440
    assert listing.listedAt > 0
    assert listing.currencies == {"metal": 0.11}
    assert listing.details == "my test description"
    assert listing.item["craftable"]
    assert listing.item["quality"]["name"] == "Unique"
    assert listing.item["quality"]["id"] == 6
    assert listing.item["tradable"]
    assert listing.item["baseName"] == "Ellis' Cap"
    assert listing.item["defindex"] == 263
    assert listing.userAgent["client"] == user_agent
    assert listing.userAgent["lastPulse"] > 0

    listing_id = listing.id


async def test_get_user_trade_url(
    aiohttp_session: ClientSession,
    backpack_tf_token: str,
    steam_id: str,
    trade_url: str,
) -> None:
    bptf = AsyncBackpackTF(aiohttp_session, backpack_tf_token, steam_id)
    listing_trade_url = await bptf.get_user_trade_url(listing_id)
    assert listing_trade_url == trade_url


async def test_create_invalid_listing(
    aiohttp_session: ClientSession, backpack_tf_token: str, steam_id: str
) -> None:
    bptf = AsyncBackpackTF(aiohttp_session, backpack_tf_token, steam_id)

    with pytest.raises(ClientResponseError):
        await bptf.create_listing(
            "-100;6",
            "buy",
            {"keys": 0, "metal": 0.11},
            "test",
        )


async def test_delete_listing(
    aiohttp_session: ClientSession, backpack_tf_token: str, steam_id: str
) -> None:
    bptf = AsyncBackpackTF(aiohttp_session, backpack_tf_token, steam_id)
    listing = await bptf.delete_listing_by_sku("263;6")
    assert isinstance(listing, bool)
    assert listing


async def test_get_snapshot(
    aiohttp_session: ClientSession, backpack_tf_token: str, steam_id: str
) -> None:
    bptf = AsyncBackpackTF(aiohttp_session, backpack_tf_token, steam_id)
    listings = await bptf.get_snapshot("Mann Co. Supply Crate Key")

    assert len(listings) > 0
    assert listings["appid"] == 440
    assert listings["sku"] == "Mann Co. Supply Crate Key"
    assert listings["createdAt"] > 0


async def test_is_banned(
    aiohttp_session: ClientSession,
    backpack_tf_token: str,
    steam_id: str,
    backpack_tf_api_key: str,
) -> None:
    bptf = AsyncBackpackTF(aiohttp_session, backpack_tf_token, steam_id)

    with pytest.raises(NeedsAPIKey):
        await bptf.is_banned(steam_id)

    bptf = AsyncBackpackTF(
        aiohttp_session,
        backpack_tf_token,
        steam_id,
        backpack_tf_api_key,
    )

    assert not await bptf.is_banned(76561198253325712)
    assert not await bptf.is_banned("76561198253325712")
    assert not await bptf.is_banned("76561198828172881")
    assert await bptf.is_banned("76561199505594824")


async def test_stop_user_agent(
    aiohttp_session: ClientSession, backpack_tf_token: str, steam_id: str
) -> None:
    bptf = AsyncBackpackTF(aiohttp_session, backpack_tf_token, steam_id)
    data = await bptf.stop_user_agent()
    assert data["status"] == "inactive"
