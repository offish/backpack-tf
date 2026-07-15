import pytest

from src.backpack_tf import (
    Currencies,
    InvalidAssetID,
    InvalidSKU,
    construct_listing,
    construct_listing_item,
    get_currencies_dict,
    get_item_hash,
)


def test_item_hash() -> None:
    assert (
        get_item_hash("Mann Co. Supply Crate Key") == "d9f847ff5dfcf78576a9fca04cbf6c07"
    )
    assert get_item_hash("Team Captain") == "a893c93bf986b65690e9e8b00bfc28e1"
    assert get_item_hash("Ellis' Cap") == "9e89a4a85aae68266ec992c22b0d52e2"


def test_currencies_dict() -> None:
    assert get_currencies_dict({"metal": 1.33}) == {"keys": 0, "metal": 1.33}
    assert get_currencies_dict({"keys": 1}) == {"keys": 1, "metal": 0}
    assert get_currencies_dict({"keys": 1, "metal": 1.11}) == {"keys": 1, "metal": 1.11}
    assert get_currencies_dict(Currencies(1, 0)) == {"keys": 1, "metal": 0}
    assert get_currencies_dict(Currencies(0, 1.22)) == {"keys": 0, "metal": 1.22}
    assert get_currencies_dict(Currencies(metal=1.44)) == {"keys": 0, "metal": 1.44}


def test_construct_listing_item() -> None:
    assert construct_listing_item("263;6") == {
        "baseName": "Ellis' Cap",
        "craftable": True,
        "quality": {"id": 6},
        "tradable": True,
    }


def test_construct_listing() -> None:
    assert construct_listing(
        "sell",
        {"keys": 1, "metal": 1.55},
        "my description",
        asset_id=13201231975,
    ) == {
        "buyout": True,
        "offers": True,
        "promoted": False,
        "currencies": {"keys": 1, "metal": 1.55},
        "details": "my description",
        "id": 13201231975,
    }

    assert construct_listing(
        "buy",
        {"keys": 1, "metal": 1.55},
        "my description",
        sku="263;6",
    ) == {
        "buyout": True,
        "offers": True,
        "promoted": False,
        "item": {
            "baseName": "Ellis' Cap",
            "craftable": True,
            "quality": {"id": 6},
            "tradable": True,
        },
        "currencies": {"keys": 1, "metal": 1.55},
        "details": "my description",
    }


def test_construct_invalid_listing() -> None:
    with pytest.raises(InvalidAssetID):
        construct_listing("sell", {"keys": 0, "metal": 1.44}, "test")

    with pytest.raises(InvalidSKU):
        construct_listing("buy", {"keys": 0, "metal": 1.44}, "test")
