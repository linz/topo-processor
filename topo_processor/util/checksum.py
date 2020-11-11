import hashlib

import multihash


def multihash_as_hex(file_path, hash_method: str = "sha2-256") -> str:
    BLOCK_SIZE = 65536  # 64kb
    file_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        data = f.read(BLOCK_SIZE)
        while len(data) > 0:
            file_hash.update(data)
            data = f.read(BLOCK_SIZE)
    return multihash.to_hex_string(multihash.encode(file_hash.digest(), hash_method))
