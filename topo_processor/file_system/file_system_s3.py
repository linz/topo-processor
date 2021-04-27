import os

import boto3
import pystac
from linz_logger import get_log

from topo_processor.stac import Asset, Collection, Item
from topo_processor.util import multihash_as_hex, time_in_ms, write_stac_metadata

from .file_system import FileSystem

s3 = boto3.client("s3")


class FileSystemS3(FileSystem):
    name = "file.system.s3"

    async def read(self):
        pass

    async def write(self, collection: Collection, target: str):
        await super().write(collection, target)

    async def list_(self):
        pass

    async def exists(self):
        pass

    async def write_asset(self, asset: Asset, target: str):
        await self.upload_file(
            file_path=asset.source_path,
            key=asset.target,
            content_type=asset.get_content_type(),
            checksum=await asset.get_checksum(),
            bucket=target.replace("s3://", ""),
        )

    async def write_item(self, item: Item, target: str):
        stac_item = item.create_stac()
        temp_item_path = os.path.join(item.collection.get_temp_dir(), item.collection.title, f"{item.id}.json")
        await write_stac_metadata(stac_item, temp_item_path)
        await self.upload_file(
            file_path=temp_item_path,
            key=f"{item.collection.title}/{item.id}.json",
            content_type="application/json",
            checksum=await item.get_checksum(temp_item_path),
            bucket=target.replace("s3://", ""),
        )
        return stac_item

    async def write_collection(self, collection: Collection, stac_collection: pystac.collection, target: str):
        temp_collection_path = os.path.join(collection.get_temp_dir(), collection.title, "collection.json")
        await write_stac_metadata(stac_collection, temp_collection_path)
        await self.upload_file(
            file_path=temp_collection_path,
            key=f"{collection.title}/collection.json",
            content_type="application/json",
            checksum=await collection.get_checksum(temp_collection_path),
            bucket=target.replace("s3://", ""),
        )

    async def upload_file(self, file_path: str, key: str, content_type: str, checksum: str, bucket: str):
        start_time = time_in_ms()
        s3.upload_file(
            Filename=file_path,
            Bucket=bucket,
            Key=key,
            ExtraArgs={"ContentType": content_type, "Metadata": {"hash": checksum}},
        )
        get_log().debug(
            "File uploaded to s3",
            duration=time_in_ms() - start_time,
            Bucket=bucket,
            Key=key,
        )
