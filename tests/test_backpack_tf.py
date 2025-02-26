from src.backpack_tf import BackpackTF

bptf = None


def test_initiate_backpack_tf(backpack_tf_token: str) -> None:
    global bptf
    bptf = BackpackTF(backpack_tf_token, "76561198253325712")


def test_construct_listing_item() -> None:
    assert bptf._construct_listing_item("263;6") == {
        "baseName": "Ellis' Cap",
        "craftable": True,
        "quality": {"id": 6},
        "tradable": True,
    }


def test_construct_listing() -> None:
    assert bptf._construct_listing(
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

    assert bptf._construct_listing(
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
