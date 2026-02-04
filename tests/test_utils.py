from src.backpack_tf import construct_listing, construct_listing_item, get_item_hash


def test_item_hash() -> None:
    assert (
        get_item_hash("Mann Co. Supply Crate Key") == "d9f847ff5dfcf78576a9fca04cbf6c07"
    )
    assert get_item_hash("Team Captain") == "a893c93bf986b65690e9e8b00bfc28e1"
    assert get_item_hash("Ellis' Cap") == "9e89a4a85aae68266ec992c22b0d52e2"


def test_construct_listing_item() -> None:
    assert construct_listing_item("263;6") == {
        "baseName": "Ellis' Cap",
        "craftable": True,
        "quality": {"id": 6},
        "tradable": True,
    }


def test_construct_listing() -> None:
    assert construct_listing(
        "263;6",
        "sell",
        {"keys": 1, "metal": 1.55},
        "my description",
        13201231975,
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
        "id": 13201231975,
    }

    assert construct_listing(
        "263;6", "buy", {"keys": 1, "metal": 1.55}, "my description"
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
