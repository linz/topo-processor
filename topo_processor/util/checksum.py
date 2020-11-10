import multihash


def multihash_as_hex(file_path: str) -> str:
    with open(file_path, "rb") as f:  # "rb" mode opens the file in binary format for reading
        contents = f.read()
        return multihash.digest(contents, "sha2-256").encode("hex").decode('UTF-8')
