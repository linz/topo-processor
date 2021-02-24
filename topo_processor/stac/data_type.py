from enum import Enum


class DataType(Enum):
    ImageryHistoric = "imagery.historic"
    ImageryAerial = "imagery.aerial"
    LidarDSM = "lidar.dsm"
    LidarDEM = "lidar.dem"
    LidarPointCloud = "lidar.pointcloud"
