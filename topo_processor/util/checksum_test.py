import os

from .checksum import multihash_as_hex


def test_mulithash_as_hex():
    file_path = os.path.join(os.getcwd(), "test_data", "tiffs", "CROWN_399_E_48.tiff")
    assert multihash_as_hex(file_path) == "1220ae1dc405490de5eebb95062a10f3d15c8314c665a1ddd004ecc67b5e9d043479"

    file_path = os.path.join(os.getcwd(), "test_data", "tiffs", "CROWN_399_E_49.tiff")
    assert multihash_as_hex(file_path) == "12202aea721911d26c1db23d11ab61ede476d894953752f148236fa960b6c12b2cd8"

    file_path = os.path.join(os.getcwd(), "test_data", "tiffs", "CROWN_399_E_50.tiff")
    assert multihash_as_hex(file_path) == "12202aea721911d26c1db23d11ab61ede476d894953752f148236fa960b6c12b2cd8"
