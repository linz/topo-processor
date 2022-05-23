from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

from linz_logger import get_log
from pystac.catalog import CatalogType

from topo_processor.file_system.transfer import transfer_file
from topo_processor.file_system.write_json import write_json
from topo_processor.metadata.data_type import DataType

if TYPE_CHECKING:
    from topo_processor.stac.collection import Collection


def transfer_collection(collection: Collection, target: str, data_type: DataType) -> None:
    stac_collection = collection.create_stac()
    files_to_transfer: dict[str, Any] = {}
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
            asset_transfer = {
                "source": asset.source_path,
                "checksum": asset.get_checksum(),
                "contentType": asset.get_content_type(),
                "target": os.path.join(target, asset.target),
            }

            if not asset.key_name:
                raise Exception(f"No asset key set for asset {asset.href}")
            else:
                stac_item.add_asset(key=asset.key_name, asset=asset.create_stac())

            existing_asset_hrefs[asset.href] = asset_transfer

        files_to_transfer[item.id] = {"images": existing_asset_hrefs}

        # pystac v1.1.0
        # Required to not add a self link with an 'absolute' link from the cwd
        json_item = stac_item.to_dict(include_self_link=False)
        if not item.collection:
            raise Exception(f"No collection set for item {item.id}")
        files_to_transfer[item.id]["stac"] = {
            "item": json_item,
            "target": os.path.join(target, item.collection.survey, f"{item.id}.json"),
        }

    # after all items have been processed generate summaries
    collection.generate_summaries(stac_collection)
    collection.update_description(stac_collection, data_type)

    try:
        collection.validate_pystac_collection(stac_collection)
    # log error as warning until TDE-353 and TDE-354 are done and handle this properly
    except Exception as e:
        get_log().error(f"Collection Validation Warning: {e}", collection_id=collection.id)
        raise Exception("Collection failed the validation. Process is stopped.") from e

    # Transfer the files
    for item_transfer in files_to_transfer.values():
        for asset_transfer in item_transfer["images"].values():
            transfer_file(
                str(asset_transfer["source"]),
                str(asset_transfer["checksum"]),
                str(asset_transfer["contentType"]),
                str(asset_transfer["target"]),
            )
        write_json(item_transfer["stac"]["item"], item_transfer["stac"]["target"])

    # pystac v1.1.0
    # Required to not add a self link with an 'absolute' link from the cwd
    json_collection = stac_collection.to_dict(include_self_link=False)

    write_json(json_collection, os.path.join(target, collection.survey, "collection.json"))
