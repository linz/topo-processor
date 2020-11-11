import hashlib

import multihash

CHUNK_SIZE = 65536  # 64kb


def multihash_as_hex(file_path: str) -> str:
    file_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        while chunk := file.read(CHUNK_SIZE):
            file_hash.update(chunk)
    return multihash.to_hex_string(multihash.encode(file_hash.digest(), "sha2-256"))
