import pystac as stac

from topo_processor.util import multihash_as_hex


async def add_asset_image(item):
    if "file" not in item.stac_item.stac_extensions:
        item.stac_item.stac_extensions.append("file")

    checksum = await multihash_as_hex(item.path)
    item.stac_item.add_asset(
        key="image",
        asset=stac.Asset(
            href=f"{item.asset_basename}.{item.asset_extension}",
            properties={
                "file:checksum": checksum,
            },
            media_type=stac.MediaType.TIFF,
        ),
    )
