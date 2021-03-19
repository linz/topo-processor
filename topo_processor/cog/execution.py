import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .command import Command


class ExecutionLocal:
    cmd: "Command"

    @staticmethod
    async def run(cmd: "Command"):
        proc = await asyncio.create_subprocess_exec(
            *cmd.to_full_command(), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise Exception(stderr.decode())
        return proc.returncode, stdout.decode(), stderr.decode()


class ExecutionDocker:
    cmd: "Command"

    @staticmethod
    async def run(cmd: "Command"):
        return await ExecutionLocal.run(cmd.to_docker())
