import hashlib

import aiofiles
import multihash

CHUNK_SIZE = 1024 * 1024  # 1MB


async def multihash_as_hex(path: str) -> str:
    file_hash = hashlib.sha256()
    async with aiofiles.open(path, "rb") as file:
        while chunk := await file.read(CHUNK_SIZE):
            file_hash.update(chunk)
    return multihash.to_hex_string(multihash.encode(file_hash.digest(), "sha2-256"))
