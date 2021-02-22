import pytest

from topo_processor.cog.command import Command


@pytest.mark.asyncio
async def test_hello_world_local(capsys):
    cmd = Command("echo")
    cmd.append_arg("Hello World Local!!!")
    return_code = await cmd.run()

    stdout, stderr = capsys.readouterr()
    assert "Hello World Local!!!" in stdout
    assert return_code == 0


@pytest.mark.asyncio
async def test_hello_world_docker(capsys):
    cmd = Command("echo", {"container": "ubuntu", "tag": "20.04"})
    cmd.append_arg("Hello World Docker!!!")
    return_code = await cmd.run()

    stdout, stderr = capsys.readouterr()
    assert "Hello World Docker!!!" in stdout
    assert return_code == 0
