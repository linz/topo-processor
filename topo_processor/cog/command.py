import os
from typing import List, Optional, TypedDict

from topo_processor.cog.execution import ExecutionDocker, ExecutionLocal


class CommandDocker(TypedDict):
    container: str
    tag: Optional[str]


class Command:
    use_docker: bool

    def __init__(self, command: str, docker_ref: CommandDocker = None):
        self.command = command
        self.arguments = []
        self.volumes = []
        self.envs = []
        if docker_ref is None:
            self.use_docker = False
        else:
            self.use_docker = True
            self.container = docker_ref.get("container", None)
            self.container_tag = docker_ref.get("tag", None)

    def arg(self, *args: str) -> "Command":
        for argument in args:
            self.arguments.append(argument)
        return self

    def mount(self, *args: str) -> "Command":
        """Mount a folder, useful only if the command is run inside of docker"""
        for volume in args:
            self.volumes.append(volume)
        return self

    def env(self, *args: str) -> "Command":
        """Only useful when using docker"""
        for env in args:
            self.envs.append(env)
        return self

    def to_full_command(self) -> List[str]:
        return [self.command] + self.arguments

    def redacted_command(self) -> List[str]:
        """Provide redacted argument string for logging which removes sensitive information"""
        redacted = []
        for arg in self.arguments:
            if arg.startswith("AWS"):
                split_arg = arg.split("=")
                arg = f"{split_arg[0]}=******"
            redacted.append(arg)
        return [self.command] + redacted

    def to_docker(self) -> "Command":
        if not self.container:
            raise Exception(f"No container found for command {self.command}")
        docker = Command("docker")
        docker.arg("run")
        for env in self.envs:
            docker.arg("--env", env)
        docker.arg("--user", f"{os.geteuid()}:{os.getegid()}")
        for volume in self.volumes:
            docker.arg("-v", f"{volume}:{volume}")
        docker.arg("--rm")

        if not self.container_tag:
            docker.arg(self.container)
        else:
            docker.arg(f"{self.container}:{self.container_tag}")

        docker.arg(self.command)
        for argument in self.arguments:
            docker.arg(argument)
        return docker

    async def run(self):
        if self.use_docker:
            return await ExecutionDocker.run(self)
        return await ExecutionLocal.run(self)
