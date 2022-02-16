class ManifestFile(object):
    path: str
    size: int
    hash: str

    def __init__(self, path: str, size: int = 0, hash: str = "") -> None:
        self.path = path
        self.size = size
        self.hash = hash
