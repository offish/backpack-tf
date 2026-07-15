from backpack_tf import BackpackTF


def main() -> None:
    bptf = BackpackTF(
        token="token",
        steam_id="76561198253325712",
        user_agent="scrapbot user agent",
    )

    # will add the lightning icon and indicate that the user is a bot
    bptf.register_user_agent()

    listing = bptf.create_buy_listing(
        "5021;6", {"metal": 57.11}, "buying keys for listed price :)"
    )

    print(listing)

    asset_id = 11543535227
    listing = bptf.create_sell_listing(
        asset_id,
        {"keys": 1, "metal": 2.11},
        "selling Siberian Sweater for 1 key, 2.11 ref",
    )

    print(listing)

    bptf.delete_listing_by_asset_id(asset_id)
    bptf.delete_listing_by_sku("5021;6")
    # or
    bptf.delete_all_listings()


if __name__ == "__main__":
    main()
