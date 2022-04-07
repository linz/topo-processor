import pytest
from moto import mock_sts

from topo_processor.geostore.environment import is_production


@mock_sts  # type: ignore
def test_is_production() -> None:
    """This test is based on the fact that mocking sts with moto set a arn to 'arn:aws:sts::123456789012:user/moto'. There is no 'nonprod' in this value."""
    assert is_production() is True
