import os

from linz_logger import get_log
from pystac.catalog import CatalogType

from topo_processor.file_system.transfer import transfer_file
from topo_processor.file_system.write_json import write_json
from topo_processor.stac import Collection


def transfer_collection(collection: Collection, target: str):
    stac_collection = collection.create_stac()
    # pystac v1.1.0
    # Required to remove cwd from collection self_href,
    # Must be come after collection.create_stac and be before stac_collection.add_item(..)
    stac_collection.catalog_type = CatalogType.SELF_CONTAINED

    for item in collection.items.values():
        stac_item = item.create_stac()

        if not item.is_valid():
            get_log().warning("Invalid item was not uploaded:", error=item.log)
            continue

        stac_collection.add_item(stac_item)
        # pystac v1.1.0
        # Required to change the pystac default of ./{id}/{id}.json
        # Must come after stac_collection.add_item(stac_item)
        stac_item.set_self_href(f"./{item.id}.json")

        existing_asset_hrefs = {}

        for asset in item.assets:
            if not asset.needs_upload:
                continue
            asset.href = f"./{item.id}{asset.file_ext()}"
            if asset.href in existing_asset_hrefs:
                raise Exception(f"{asset.href} already exists.")
            transfer_file(
                asset.source_path, asset.get_checksum(), asset.get_content_type(), os.path.join(target, asset.target)
            )
            stac_item.add_asset(
                key=(asset.get_content_type() if asset.get_content_type() else asset.file_ext()), asset=asset.create_stac()
            )
            existing_asset_hrefs[asset.href] = asset

        # pystac v1.1.0
        # Required to not add a self link with an 'absolute' link from the cwd
        json_item = stac_item.to_dict(include_self_link=False)
        write_json(json_item, os.path.join(target, item.collection.title, f"{item.id}.json"))

    # pystac v1.1.0
    # Required to not add a self link with an 'absolute' link from the cwd
    json_collection = stac_collection.to_dict(include_self_link=False)
    write_json(json_collection, os.path.join(target, collection.title, "collection.json"))
