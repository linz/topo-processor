import os

from linz_logger import get_log

from topo_processor.file_system.transfer import transfer_file
from topo_processor.file_system.write_json import write_json
from topo_processor.stac import Collection


async def transfer_collection(collection: Collection, target: str):
    stac_collection = collection.create_stac()
    stac_collection.set_self_href("./collection.json")

    for item in collection.items.values():
        stac_item = item.create_stac()

        if not item.is_valid():
            get_log().warning("Invalid item was not uploaded:", error=item.log)
            continue

        stac_collection.add_item(stac_item)
        # this line must come after stac_collection.add_item(stac_item) pystac v5.6.0
        stac_item.set_self_href(f"./{item.id}.json")

        existing_asset_hrefs = {}

        for asset in item.assets:
            if not asset.needs_upload:
                continue
            asset.href = f"./{item.id}{asset.file_ext()}"
            if asset.href in existing_asset_hrefs:
                raise Exception(f"{asset.href} already exists.")
            transfer_file(
                asset.source_path, await asset.get_checksum(), asset.get_content_type(), os.path.join(target, asset.target)
            )
            stac_item.add_asset(
                key=(asset.get_content_type() if asset.get_content_type() else asset.file_ext()), asset=asset.create_stac()
            )
            existing_asset_hrefs[asset.href] = asset

        # 06/07/2021: Workaround for pystac v1.0.0-beta.2
        json_item = stac_item.to_dict()
        json_item["stac_version"] = "1.0.0"
        write_json(json_item, os.path.join(target, item.collection.title, f"{item.id}.json"))

    # 06/07/2021: Workaround for pystac v1.0.0-beta.2
    json_collection = stac_collection.to_dict()
    json_collection["type"] = "Collection"
    json_collection["stac_version"] = "1.0.0"

    write_json(json_collection, os.path.join(target, collection.title, "collection.json"))
