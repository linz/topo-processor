import shutil
from tempfile import mkdtemp
from typing import Generator

import pystac
import pytest

from topo_processor.stac.iter_errors_validator import IterErrorsValidator

#pystac.validation.set_validator(IterErrorsValidator())


def pytest_addoption(parser) -> None:  # type: ignore
    parser.addoption("--slow", action="store_true", default=False, help="run slow tests")


def pytest_runtest_setup(item) -> None:  # type: ignore
    if "slow" in item.keywords and not item.config.getoption("--slow"):
        pytest.skip("need --slow option to run this test")


@pytest.fixture(autouse=True)
def setup() -> Generator[str, None, None]:
    """
    This function creates a temporary directory and deletes it after each test.
    See following link for details:
    https://docs.pytest.org/en/stable/fixture.html#yield-fixtures-recommended
    """
    target = mkdtemp()
    yield target
    shutil.rmtree(target)
