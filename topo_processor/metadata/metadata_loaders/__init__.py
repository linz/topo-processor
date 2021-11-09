from .metadata_loader_imagery_historic import MetadataLoaderImageryHistoric
from .metadata_loader_repo import MetadataLoaderRepository
from .metadata_loader_tiff import MetadataLoaderTiff

metadata_loader_repo = MetadataLoaderRepository()
metadata_loader_repo.append(MetadataLoaderImageryHistoric())
metadata_loader_repo.append(MetadataLoaderTiff())

metadata_loader_imagery_historic = MetadataLoaderImageryHistoric()
metadata_loader_tiff = MetadataLoaderTiff()
