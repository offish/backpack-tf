from hashlib import md5

from tf2_utils import sku_is_craftable, sku_to_quality
from tf2_utils.instances import schema

from .classes import Currencies
from .exceptions import InvalidIntent, NeedsAPIKey, NoTokenProvided


def get_item_hash(item_name: str) -> str:
    return md5(item_name.encode()).hexdigest()


def get_sku_item_hash(sku: str) -> str:
    item_name = schema.sku_to_base_name(sku)
    return get_item_hash(item_name)


def construct_listing_item(sku: str) -> dict:
    return {
        "baseName": schema.sku_to_base_name(sku),
        "craftable": sku_is_craftable(sku),
        "tradable": True,
        "quality": {"id": sku_to_quality(sku)},
    }


def construct_listing(
    sku: str, intent: str, currencies: dict, details: str, asset_id: int = 0
) -> dict:
    if intent not in ["buy", "sell"]:
        raise InvalidIntent(f"{intent} must be buy or sell")

    listing = {
        "item": construct_listing_item(sku),
        "buyout": True,
        "offers": True,
        "promoted": False,
        "details": details,
        "currencies": Currencies(**currencies).__dict__,
    }

    if intent == "sell":
        listing["id"] = asset_id

    return listing


def needs_token(func):
    def wrapper(self, *args, **kwargs):
        if not self._token:
            raise NoTokenProvided("Set a token to use this method")

        return func(self, *args, **kwargs)

    return wrapper


def needs_api_key(func):
    def wrapper(self, *args, **kwargs):
        if not self._api_key:
            raise NeedsAPIKey("Set an API key to use this method")

        return func(self, *args, **kwargs)

    return wrapper
