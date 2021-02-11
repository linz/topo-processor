import os

import pytest

from topo_processor.cog.create_cog import create_cog


@pytest.mark.asyncio
async def test_create_cog():
    tiff_path = os.path.join(os.getcwd(), "test_data", "tiffs", "CROWN_399_E_49.tiff")
    output_path = os.getcwd()
    await create_cog(tiff_path, output_path)

    output_cog_path = os.path.join(output_path, "CROWN_399_E_49.tiff.tif.deflate.cog.tiff")
    assert os.path.isfile(output_cog_path)
    if os.path.isfile(output_cog_path):
        os.remove(output_cog_path)
