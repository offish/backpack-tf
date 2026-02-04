import requests
from aiohttp import ClientSession

from . import __title__, __version__
from .classes import Listing
from .exceptions import NeedsAPIKey, UserNotFound
from .utils import (
    construct_listing,
    get_item_hash,
    get_sku_item_hash,
    needs_api_key,
    needs_token,
)


class BackpackTF:
    def __init__(
        self,
        token: str,
        steam_id: str,
        api_key: str = None,
        user_agent: str = "Listing goin' up!",
    ) -> None:
        self._token = token
        self._steam_id = steam_id
        self._api_key = api_key

        library = f"{__title__} v{__version__}"
        self._headers = {"User-Agent": f"{user_agent} | {library}"}

    @needs_token
    def request(self, method: str, endpoint: str, params: dict = {}, **kwargs) -> dict:
        params["token"] = self._token

        if self._api_key:
            params["key"] = self._api_key

        url = "https://api.backpack.tf/api" + endpoint

        response = requests.request(
            method,
            url,
            params=params,
            headers=self._headers,
            **kwargs,
        )
        response.raise_for_status()

        return response.json()

    @needs_api_key
    def is_banned(self, steam_id: str | int) -> bool:
        if isinstance(steam_id, int):
            steam_id = str(steam_id)

        endpoint = "/users/info/v1"
        params = {"steamids": steam_id}
        response = self.request("GET", endpoint, params)

        if "users" not in response or steam_id not in response["users"]:
            raise UserNotFound(f"User {steam_id} not found {response}")

        user = response["users"][steam_id]
        return user.get("bans") is not None

    def get_snapshot(self, item_name: str) -> list[dict]:
        endpoint = "/classifieds/listings/snapshot"
        params = {"appid": 440, "sku": item_name}
        return self.request("GET", endpoint, params)

    def get_listing(self, listing_id: str) -> dict:
        endpoint = f"/v2/classifieds/listings/{listing_id}"
        return self.request("GET", endpoint)

    def get_user_trade_url(self, listing_id: str) -> str:
        user = self.get_listing(listing_id).get("user", {})
        return user.get("tradeOfferUrl", "")

    def get_listings(self, skip: int = 0, limit: int = 100) -> dict:
        return self.request(
            "GET", "/v2/classifieds/listings", {"skip": skip, "limit": limit}
        )

    def create_listing(
        self, sku: str, intent: str, currencies: dict, details: str, asset_id: int = 0
    ) -> Listing:
        listing = construct_listing(sku, intent, currencies, details, asset_id)
        response = self.request("POST", "/v2/classifieds/listings", json=listing)
        return Listing(**response)

    def create_listings(self, listings: list[dict]) -> list[Listing]:
        to_list = [construct_listing(**listing) for listing in listings]
        response = self.request("POST", "/v2/classifieds/listings/batch", json=to_list)
        return [Listing(**listing["result"]) for listing in response]

    def delete_all_listings(self) -> dict:
        return self.request("DELETE", "/v2/classifieds/listings")

    def delete_listing(self, listing_id: str) -> dict:
        return self.request("DELETE", f"/v2/classifieds/listings/{listing_id}")

    def delete_listing_by_asset_id(self, asset_id: int) -> dict:
        listing_id = f"440_{asset_id}"
        return self.delete_listing(listing_id)

    def delete_listing_by_item_name(
        self, item_name: str, is_hash: bool = False
    ) -> dict:
        item_hash = item_name

        if not is_hash:
            item_hash = get_item_hash(item_name)

        listing_id = f"440_{self._steam_id}_{item_hash}"
        return self.delete_listing(listing_id)

    def delete_listing_by_sku(self, sku: str) -> dict:
        item_hash = get_sku_item_hash(sku)
        return self.delete_listing_by_item_name(item_hash, is_hash=True)

    def register_user_agent(self) -> dict:
        return self.request("POST", "/agent/pulse")

    def get_user_agent_status(self) -> dict:
        return self.request("POST", "/agent/status")

    def stop_user_agent(self) -> dict:
        return self.request("POST", "/agent/stop")


class AsyncBackpackTF:
    def __init__(
        self,
        session: ClientSession,
        token: str,
        steam_id: str,
        api_key: str = None,
        user_agent: str = "Listing goin' up!",
    ) -> None:
        self.session = session
        self._token = token
        self._steam_id = steam_id
        self._api_key = api_key

        library = f"{__title__} v{__version__}"
        self._headers = {"User-Agent": f"{user_agent} | {library}"}

    async def request(
        self, method: str, endpoint: str, params: dict = {}, **kwargs
    ) -> dict:
        url = "https://api.backpack.tf/api" + endpoint
        params["token"] = self._token

        if self._api_key:
            params["key"] = self._api_key

        async with self.session.request(
            method,
            url,
            params=params,
            headers=self._headers,
            **kwargs,
        ) as resp:
            resp.raise_for_status()
            response = await resp.json()

        return response

    async def is_banned(self, steam_id: str | int) -> bool:
        if self._api_key is None:
            raise NeedsAPIKey("Set an API key to use this method")

        if isinstance(steam_id, int):
            steam_id = str(steam_id)

        endpoint = "/users/info/v1"
        params = {"steamids": steam_id}
        response = await self.request("GET", endpoint, params)

        if "users" not in response or steam_id not in response["users"]:
            raise UserNotFound(f"User {steam_id} not found {response}")

        user = response["users"][steam_id]
        return user.get("bans") is not None

    async def get_snapshot(self, item_name: str) -> list[dict]:
        endpoint = "/classifieds/listings/snapshot"
        params = {"appid": 440, "sku": item_name}
        return await self.request("GET", endpoint, params)

    async def get_listing(self, listing_id: str) -> dict:
        return await self.request("GET", f"/v2/classifieds/listings/{listing_id}")

    async def get_user_trade_url(self, listing_id: str) -> str:
        listing = await self.get_listing(listing_id)
        user = listing.get("user", {})
        return user.get("tradeOfferUrl", "")

    async def get_listings(self, skip: int = 0, limit: int = 100) -> dict:
        endpoint = "/v2/classifieds/listings"
        params = {"skip": skip, "limit": limit}
        return await self.request("GET", endpoint, params)

    async def create_listing(
        self, sku: str, intent: str, currencies: dict, details: str, asset_id: int = 0
    ) -> Listing:
        listing = construct_listing(sku, intent, currencies, details, asset_id)
        response = await self.request("POST", "/v2/classifieds/listings", json=listing)
        return Listing(**response)

    async def create_listings(self, listings: list[dict]) -> list[Listing]:
        endpoint = "/v2/classifieds/listings/batch"
        to_list = [construct_listing(**listing) for listing in listings]
        response = await self.request("POST", endpoint, json=to_list)
        return [Listing(**listing["result"]) for listing in response]

    async def delete_all_listings(self) -> dict:
        return await self.request("DELETE", "/v2/classifieds/listings")

    async def delete_listing(self, listing_id: str) -> dict:
        return await self.request("DELETE", f"/v2/classifieds/listings/{listing_id}")

    async def delete_listing_by_asset_id(self, asset_id: int) -> dict:
        listing_id = f"440_{asset_id}"
        return await self.delete_listing(listing_id)

    async def delete_listing_by_item_name(
        self, item_name: str, is_hash: bool = False
    ) -> dict:
        item_hash = item_name

        if not is_hash:
            item_hash = get_item_hash(item_name)

        listing_id = f"440_{self._steam_id}_{item_hash}"
        return await self.delete_listing(listing_id)

    async def delete_listing_by_sku(self, sku: str) -> dict:
        item_hash = get_sku_item_hash(sku)
        return await self.delete_listing_by_item_name(item_hash, is_hash=True)

    async def register_user_agent(self) -> dict:
        return await self.request("POST", "/agent/pulse")

    async def get_user_agent_status(self) -> dict:
        return await self.request("POST", "/agent/status")

    async def stop_user_agent(self) -> dict:
        return await self.request("POST", "/agent/stop")
