from .metadata_loader_checksum import MetadataLoaderChecksum
from .metadata_loader_imagery_historic import MetadataLoaderImageryHistoric
from .metadata_loader_repo import MetadataLoaderRepository
from .metadata_loader_tiff import MetadataLoaderTiff

repo = MetadataLoaderRepository()
repo.append(MetadataLoaderImageryHistoric())
repo.append(MetadataLoaderTiff())
repo.append(MetadataLoaderChecksum())
