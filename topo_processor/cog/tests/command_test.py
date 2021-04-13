import pytest

from topo_processor.cog.command import Command


@pytest.mark.asyncio
async def test_hello_world_local():
    cmd = Command("echo")
    cmd.arg("Hello World Local!!!")
    return_code, stdout, stderr = await cmd.run()
    assert stdout == "Hello World Local!!!\n"
    assert stderr == ""
    assert return_code == 0


@pytest.mark.asyncio
async def test_hello_world_docker(mocker):
    cmd = Command("/bin/echo", {"container": "busybox", "tag": "latest"})
    cmd.arg("Hello World Docker!!!")
    mocker.patch("topo_processor.cog.execution.ExecutionLocal.run", return_value=[0, "Hello World Docker!!!\n", ""])
    return_code, stdout, _ = await cmd.run()
    assert stdout == "Hello World Docker!!!\n"
    assert return_code == 0
