import pytest


def pytest_addoption(parser):
    parser.addoption("--slow", action="store_true", default=False, help="run slow tests")


def pytest_runtest_setup(item):
    if "slow" in item.keywords and not item.config.getoption("--slow"):
        pytest.skip("need --slow option to run this test")
