from .metadata_loader_checksum import MetadataLoaderChecksum
from .metadata_loader_imagery_historic import MetadataLoaderImageryHistoric
from .metadata_loader_repo import MetadataLoaderRepository
from .metadata_loader_tiff import MetadataLoaderTiff

loader_repo = MetadataLoaderRepository()
loader_repo.append(MetadataLoaderImageryHistoric())
loader_repo.append(MetadataLoaderTiff())
loader_repo.append(MetadataLoaderChecksum())
