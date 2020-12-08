import os

from .checksum import multihash_as_hex


def test_mulithash_as_hex():
    file_path = os.path.join(os.getcwd(), "test_data", "tiffs", "CROWN_399_E_48.tiff")
    assert multihash_as_hex(file_path) == "1220d1bed69013d3dbcf4b1ef90016d77be83ad9b1759865ef5f9969ed540f902f53"

    file_path = os.path.join(os.getcwd(), "test_data", "tiffs", "CROWN_399_E_49.tiff")
    assert multihash_as_hex(file_path) == "1220d3e42a62bb123eeeb96358f1e4ed46d20b1a329a4738dd643d27623ba8452957"

    file_path = os.path.join(os.getcwd(), "test_data", "tiffs", "CROWN_399_E_50.tiff")
    assert multihash_as_hex(file_path) == "1220d3e42a62bb123eeeb96358f1e4ed46d20b1a329a4738dd643d27623ba8452957"
