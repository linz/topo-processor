import os

import pytest

from topo_processor.cog.create_cog import create_cog


@pytest.fixture(autouse=True)
def delete_cog():
    """Automatically runs before and after each test"""
    yield
    output_path = os.path.join(os.getcwd(), "CROWN_399_E_49.tiff.lzw.cog.tiff")
    if os.path.isfile(output_path):
        os.remove(output_path)


@pytest.mark.asyncio
async def test_cog_command():
    input_path = "fake_input_dir/fake_input.tiff"
    output_dir = "fake_output_dir"
    compression_method = "LZW"
    output_path = os.path.join(output_dir, f"{os.path.basename(input_path)}.{compression_method}.cog.tiff")

    cmd = create_cog(input_path, output_path, compression_method)
    assert cmd.to_full_command() == [
        "gdal_translate",
        "fake_input_dir/fake_input.tiff",
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
