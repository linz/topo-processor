from enum import Enum
from typing import Dict


class DataType(str, Enum):
    IMAGERY_HISTORIC = "imagery.historic"
    IMAGERY_AERIAL = "imagery.aerial"
    LIDAR_DSM = "lidar.dsm"
    LIDAR_DEM = "lidar.dem"
    LIDAR_POINT_CLOUD = "lidar.pointcloud"
    SURVEY_FOOTPRINT_HISTORIC = "survey.footprint.historic"


data_type_layer: Dict[str, str] = {DataType.IMAGERY_HISTORIC: "51002", DataType.SURVEY_FOOTPRINT_HISTORIC: "51000"}


def get_layer_id(data_type: str) -> str:
    return data_type_layer[data_type]
