from shutil import copyfile

from topo_processor.stac.collection import Collection
from topo_processor.stac.item import Item
from topo_processor.util import write_stac_object


async def upload_to_local_disk(collection: Collection, target: str):
    for item in collection.items:
        await write_stac_object(item, f"{target}/{item.item_output_path}")  # for metadata
        await copy_item_data_file(item, target)  # for data
    await write_stac_object(collection, f"{target}/{collection.collection_output_path}")


async def copy_item_data_file(stac_item: Item, target: str):
    # TODO this is not async
    if stac_item.transformed_data_path:
        copyfile(
            stac_item.transformed_data_path, f"{target}/{stac_item.asset_basename}.{stac_item.transformed_asset_extension}"
        )
    else:
        copyfile(stac_item.path, f"{target}/{stac_item.asset_basename}.{stac_item.asset_extension}")
