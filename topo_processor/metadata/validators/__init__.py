from .metadata_validator_repo import MetadataValidatorRepository
from .metadata_validator_tiff import MetadataValidatorTiff

validator_repo = MetadataValidatorRepository()
validator_repo.append(MetadataValidatorTiff())
