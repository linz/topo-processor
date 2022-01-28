from enum import Enum


class DataType(str, Enum):
    IMAGERY_HISTORIC = "imagery.historic"
    IMAGERY_AERIAL = "imagery.aerial"
    LIDAR_DSM = "lidar.dsm"
    LIDAR_DEM = "lidar.dem"
    LIDAR_POINT_CLOUD = "lidar.pointcloud"
