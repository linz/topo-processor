import subprocess
from typing import TYPE_CHECKING

from linz_logger import get_log

from topo_processor.util.time import time_in_ms

if TYPE_CHECKING:
    from .command import Command


class ExecutionLocal:
    cmd: "Command"

    @staticmethod
    def run(cmd: "Command"):
        start_time = time_in_ms()

        proc = subprocess.run(cmd.to_full_command(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            get_log().trace("Ran command failed", command=cmd.redacted_command(), duration=time_in_ms() - start_time)
            raise Exception(proc.stderr.decode())
        get_log().trace("Ran command succeeded", command=cmd.redacted_command(), duration=time_in_ms() - start_time)
        return proc.returncode, proc.stdout.decode(), proc.stderr.decode()


class ExecutionDocker:
    cmd: "Command"

    @staticmethod
    def run(cmd: "Command"):
        return ExecutionLocal.run(cmd.to_docker())
