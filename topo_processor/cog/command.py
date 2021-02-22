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
        if docker_ref is None:
            self.use_docker = False
        else:
            self.use_docker = True
            self.container = docker_ref.get("container", None)
            self.container_tag = docker_ref.get("tag", None)

    def append_arg(self, *args: str) -> "Command":
        for argument in args:
            self.arguments.append(argument)
        return self

    def mount(self, *args: str) -> "Command":
        """Mount a folder, useful only if the command is run inside of docker"""
        for volume in args:
            self.volumes.append(volume)
        return os.sendfile

    def to_full_command(self) -> List[str]:
        return [self.command] + self.arguments

    def to_docker(self) -> "Command":
        if not self.container:
            raise Exception(f"No container found for command {self.command}")
        docker = Command("docker")
        docker.append_arg("run")
        docker.append_arg("--user", f"{os.geteuid()}:{os.getegid()}")
        for volume in self.volumes:
            docker.mount(volume)
            docker.append_arg("-v", f"{volume}:{volume}")
        docker.append_arg("--rm")

        if not self.container_tag:
            docker.append_arg(self.container)
        else:
            docker.append_arg(f"{self.container}:{self.container_tag}")

        docker.append_arg(self.command)
        for argument in self.arguments:
            docker.append_arg(argument)
        return docker

    async def run(self):
        if self.use_docker:
            return await ExecutionDocker.run(self)
        return await ExecutionLocal.run(self)
