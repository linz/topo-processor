import os

import pytest

from topo_processor.cog.create_cog import to_gdal_command


@pytest.fixture(autouse=True)
def delete_cog():
    """Automatically runs before and after each test"""
    yield
    output_path = os.path.join(os.getcwd(), "CROWN_399_E_49.tiff.LZW.cog.tiff")
    if os.path.isfile(output_path):
        os.remove(output_path)


@pytest.mark.asyncio
async def test_gdal_command():
    input_file = "fake_input.tiff"
    output_dir = "fake_output_dir"
    compression_method = "LZW"
    cmd = to_gdal_command(input_file, output_dir, compression_method)
    assert cmd.to_full_command() == [
        "gdal_translate",
        "fake_input.tiff",
        "-of",
        "COG",
        "-co",
        "COMPRESS=LZW",
        "-co",
        "NUM_THREADS=ALL_CPUS",
        "-co",
        "PREDICTOR=2",
        "fake_output_dir/fake_input.tiff.LZW.cog.tiff",
    ]
