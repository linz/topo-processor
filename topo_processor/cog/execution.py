import asyncio
from typing import TYPE_CHECKING

from linz_logger import get_log

from topo_processor.util import time_in_ms

if TYPE_CHECKING:
    from .command import Command


class ExecutionLocal:
    cmd: "Command"

    @staticmethod
    async def run(cmd: "Command"):
        start_time = time_in_ms()
        proc = await asyncio.create_subprocess_exec(
            *cmd.to_full_command(), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            get_log().trace("Ran command failed", command=cmd.to_full_command(), duration=time_in_ms() - start_time)
            raise Exception(stderr.decode())
        get_log().trace("Ran command succeeded", command=cmd.to_full_command(), duration=time_in_ms() - start_time)
        return proc.returncode, stdout.decode(), stderr.decode()


class ExecutionDocker:
    cmd: "Command"

    @staticmethod
    async def run(cmd: "Command"):
        return await ExecutionLocal.run(cmd.to_docker())
