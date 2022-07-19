import os

from topo_processor.cog.command import Command


def geopackage_to_csv(input_path: str, output_path: str) -> Command:
    if os.environ.get("IS_DOCKER") == "true":
        cmd = Command("ogr2ogr")
    else:
        cmd = Command("ogr2ogr", {"container": "osgeo/gdal", "tag": "ubuntu-small-3.5.0"})

    cmd.mount(input_path)
    cmd.mount(os.path.dirname(output_path))
    cmd.arg("-f", "CSV")
    cmd.arg("-lco", "GEOMETRY=AS_WKT")
    cmd.arg(output_path)
    cmd.arg(input_path)
    return cmd
