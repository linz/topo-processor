import pytest

from topo_processor.cog.create_cog import create_cog


@pytest.mark.asyncio
async def test_cog_command():
    input_path = "fake_input_dir/fake_input.tiff"
    output_path = "fake_input_dir/fake_output.tiff"

    cmd = create_cog(input_path, output_path, "LZW")
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
        "fake_input_dir/fake_output.tiff",
    ]
