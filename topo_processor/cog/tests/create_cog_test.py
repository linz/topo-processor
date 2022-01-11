import pytest

from topo_processor.cog.create_cog import create_cog


def test_cog_command():
    input_path = "fake_input_dir/fake_input.tiff"
    output_path = "fake_input_dir/fake_output.tiff"

    cmd = create_cog(input_path, output_path, "LZW", "JPEG")
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
        "-co",
        "OVERVIEW_COMPRESS=JPEG",
        "-co",
        "BIGTIFF=YES",
        "-co",
        "OVERVIEW_RESAMPLING=LANCZOS",
        "-co",
        "BLOCKSIZE=512",
        "-co",
        "OVERVIEW_QUALITY=90",
        "-co",
        "SPARSE_OK=TRUE",
        "-co",
        "GDAL_DISABLE_READDIR_ON_OPEN=EMPTY_DIR",
        "fake_input_dir/fake_output.tiff",
    ]
