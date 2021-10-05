import hashlib

import multihash

from topo_processor.file_system.get_fs import get_fs

CHUNK_SIZE = 1024 * 1024  # 1MB


def multihash_as_hex(path: str) -> str:
    file_hash = hashlib.sha256()
    with get_fs(path).open(path, "rb") as file:
        while chunk := file.read(CHUNK_SIZE):
            file_hash.update(chunk)
    return multihash.to_hex_string(multihash.encode(file_hash.digest(), "sha2-256"))
