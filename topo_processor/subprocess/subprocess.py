import asyncio

from linz_logger import get_log

from topo_processor.util.time import time_in_ms


async def run(cmd: str):
    start_time = time_in_ms()
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if stderr:
        raise Exception(stderr.decode())
    get_log().debug(
        "Subprocess Created",
        stdout=stdout.decode(),
        duration=time_in_ms() - start_time,
    )
