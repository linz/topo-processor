from __future__ import annotations

import os
from typing import TYPE_CHECKING

from linz_logger import get_log
from pystac.catalog import CatalogType

from topo_processor.file_system.transfer import transfer_file
from topo_processor.file_system.write_json import write_json

if TYPE_CHECKING:
    from topo_processor.stac.collection import Collection


def transfer_collection(collection: Collection, target: str) -> None:
    stac_collection = collection.create_stac()
    # pystac v1.1.0
    # Required to remove cwd from collection self_href,
    # Must be come after collection.create_stac and be before stac_collection.add_item(..)
    stac_collection.catalog_type = CatalogType.SELF_CONTAINED

    for item in collection.items.values():
        if not item.is_valid():
            get_log().warning("Invalid item was not uploaded:", error=item.log)
            continue
        if item.log:
            get_log().warning(f"Item {item.id} contains warnings:", error=item.log)

        stac_item = item.create_stac()
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
            if not asset.target:
                raise Exception(f"No asset target set for asset {asset.href}")
            transfer_file(
                asset.source_path, asset.get_checksum(), asset.get_content_type(), os.path.join(target, asset.target)
            )
            if not asset.key_name:
                raise Exception(f"No asset key set for asset {asset.href}")
            else:
                stac_item.add_asset(key=asset.key_name, asset=asset.create_stac())

            existing_asset_hrefs[asset.href] = asset

        # pystac v1.1.0
        # Required to not add a self link with an 'absolute' link from the cwd

        json_item = stac_item.to_dict(include_self_link=False)
        if not item.collection:
            raise Exception(f"No collection set for item {item.id}")
        write_json(json_item, os.path.join(target, item.collection.title, f"{item.id}.json"))

    # after all items have been processed generate summaries
    collection.generate_summaries(stac_collection)

    # pystac v1.1.0
    # Required to not add a self link with an 'absolute' link from the cwd
    json_collection = stac_collection.to_dict(include_self_link=False)

    write_json(json_collection, os.path.join(target, collection.title, "collection.json"))
