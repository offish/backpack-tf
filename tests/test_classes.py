from src.backpack_tf import Currencies, Listing


def test_currencies() -> None:
    assert Currencies().__dict__ == {"keys": 0, "metal": 0.0}
    assert Currencies(1, 1.5).__dict__ == {"keys": 1, "metal": 1.5}
    assert Currencies(**{"metal": 10.55}).__dict__ == {"keys": 0, "metal": 10.55}
    assert Currencies(**{"keys": 2}).__dict__ == {"keys": 2, "metal": 0}
    assert Currencies(metal=10.55).__dict__ == {"keys": 0, "metal": 10.55}


def test_listing_allows_optional_deal() -> None:
    listing_without_deal = Listing(
        id="id",
        steamid="steamid",
        appid=440,
        currencies={"metal": 1.0},
        value={"raw": 1.0},
        details="details",
        listedAt=1,
        bumpedAt=1,
        intent="buy",
        count=1,
        status="active",
        source="user",
        item={"defindex": 5021},
    )

    assert listing_without_deal.deal == {}

    listing_with_deal = Listing(
        id="id",
        steamid="steamid",
        appid=440,
        currencies={"metal": 1.0},
        value={"raw": 1.0},
        details="details",
        listedAt=1,
        bumpedAt=1,
        intent="buy",
        count=1,
        status="active",
        source="user",
        item={"defindex": 5021},
        deal={"percent": 0.11, "value": 33.88},
    )

    assert listing_with_deal.deal == {"percent": 0.11, "value": 33.88}
