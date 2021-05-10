import asyncio
import os

import boto3
import pystac
from linz_logger import get_log

from topo_processor.stac import Collection
from topo_processor.util import multihash_as_hex, time_in_ms

s3 = boto3.client("s3")


async def upload_to_s3(collection: Collection, target: str):
    await upload_items(collection, target)
    await upload_collection(collection, target)


async def upload_items(collection: Collection, target: str):
    to_upload = []
    for item in collection.items.values():
        # for metadata
        pystac.write_file(obj=item, dest_href=os.path.join(item.temp_dir, item.parent, f"{item.id}{item.file_ext}"))
        checksum = await multihash_as_hex(os.path.join(item.temp_dir, item.parent, f"{item.id}{item.file_ext}"))
        to_upload.append(
            upload_file(
                os.path.join(collection.temp_dir, item.parent, f"{item.id}{item.file_ext}"),
                os.path.join(item.parent, f"{item.id}{item.file_ext}"),
                item.content_type,
                checksum,
                target,
            )
        )
        # for asset
        for asset in item.assets:
            to_upload.append(
                upload_file(
                    asset["path"],
                    asset["href"],
                    asset["content_type"],
                    asset["properties"]["file:checksum"],
                    target,
                )
            )
    await asyncio.gather(*to_upload)


async def upload_collection(collection: Collection, target: str):
    # TODO: collection has no temp dir
    pystac.write_file(obj=collection, dest_href=os.path.join(collection.temp_dir, collection.metadata_path))
    checksum = await multihash_as_hex(os.path.join(collection.temp_dir, collection.metadata_path))
    await upload_file(
        os.path.join(collection.temp_dir, collection.metadata_path),
        collection.metadata_path,
        collection.content_type,
        checksum,
        target,
    )


async def upload_file(file_path: str, key: str, content_type: str, hash_value: str, bucket: str):
    start_time = time_in_ms()
    s3.upload_file(
        Filename=file_path,
        Bucket=bucket,
        Key=key,
        ExtraArgs={"ContentType": content_type, "Metadata": {"hash": hash_value}},
    )
    get_log().debug(
        "S3 Multipart File Uploaded",
        duration=time_in_ms() - start_time,
        Bucket=bucket,
        Key=key,
    )
