import subprocess
from typing import Optional
from commander.expected import ExpectedResult, NoStdErr, SuccessCode
from commander.arguments import CommandArg


class Command:
    def __init__(
        self,
        name: str,
        arguments: Optional[list[CommandArg]] = None,
        expect: Optional[list[ExpectedResult]] = None,
    ) -> None:
        self.stdout = ""
        self.stderr = ""
        self.code: Optional[int] = None
        self.name = name
        self.arguments: list[CommandArg] = arguments or []
        self.expect: list[ExpectedResult] = expect or [NoStdErr(), SuccessCode()]

    def __str__(self) -> str:
        return f"{self.name} {' '.join(arg.fmt_str() for arg in self.arguments)}"

    def as_list(self) -> list[str]:
        return [self.name, *sum((arg.fmt_list() for arg in self.arguments), [])]

    def execute(self) -> None:
        command = [self.name, *sum((arg.fmt_list() for arg in self.arguments), [])]
        process = subprocess.run(command, capture_output=True, text=True, shell=True)
        self.stdout = process.stdout
        self.stderr = process.stderr
        self.code = process.returncode

    def check(self) -> bool:
        return all(awaited.check(self) for awaited in self.expect)
