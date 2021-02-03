import pytest

from .subprocess import run


@pytest.mark.asyncio
async def test_run():
    await run("echo BLAH")


@pytest.mark.asyncio
async def test_run_fail():
    with pytest.raises(Exception, match=r"/bin/sh: 1: ecHo: not found\n"):
        await run("ecHo BLAH")
