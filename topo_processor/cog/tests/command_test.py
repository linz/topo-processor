import asyncio

from topo_processor.cog.command import Command


def test_hello_world_local():
    cmd = Command("echo")
    cmd.arg("Hello World Local!!!")
    return_code, stdout, stderr = asyncio.run(cmd.run())
    assert stdout == "Hello World Local!!!\n"
    assert stderr == ""
    assert return_code == 0


def test_hello_world_docker():
    cmd = Command("/bin/echo", {"container": "busybox", "tag": "latest"})
    cmd.arg("Hello World Docker!!!")
    return_code, stdout, stderr = asyncio.run(cmd.run())
    assert stdout == "Hello World Docker!!!\n"
    assert return_code == 0
