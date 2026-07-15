from hashlib import md5

from tf2_utils import sku_is_craftable, sku_to_quality
from tf2_utils.instances import schema

from .classes import Currencies
from .exceptions import (
    InvalidAssetID,
    InvalidIntent,
    InvalidSKU,
    NeedsAPIKey,
    NoTokenProvided,
)


def get_item_hash(item_name: str) -> str:
    return md5(item_name.encode()).hexdigest()


def get_sku_item_hash(sku: str) -> str:
    item_name = schema.sku_to_base_name(sku)
    return get_item_hash(item_name)


def get_currencies_dict(currencies: dict | Currencies) -> dict:
    if isinstance(currencies, Currencies):
        return currencies.__dict__

    return Currencies(**currencies).__dict__


def construct_listing_item(sku: str) -> dict:
    return {
        "baseName": schema.sku_to_base_name(sku),
        "craftable": sku_is_craftable(sku),
        "tradable": True,
        "quality": {"id": sku_to_quality(sku)},
    }


def construct_listing(
    intent: str,
    currencies: dict | Currencies,
    details: str,
    sku: str = None,
    asset_id: int | str = 0,
) -> dict:
    if intent not in ["buy", "sell"]:
        raise InvalidIntent(f"{intent} must be buy or sell")

    if intent == "buy" and not sku:
        raise InvalidSKU("cannot create a buy listing without sku")

    if intent == "sell" and not asset_id:
        raise InvalidAssetID("cannot construct sell listing without asset_id")

    listing = {
        "buyout": True,
        "offers": True,
        "promoted": False,
        "details": details,
        "currencies": get_currencies_dict(currencies),
    }

    if intent == "buy":
        listing["item"] = construct_listing_item(sku)
    else:
        listing["id"] = int(asset_id)

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
