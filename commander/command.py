import subprocess
from typing import Any, Optional
from commander.expected import AbstractExpectedResult, NoStdErr, SuccessCode
from commander.arguments import AbstractArg
from commander.exceptions import UnexpectedResultError


class Command:
    def __init__(
        self,
        command: str,
        arguments: Optional[list[AbstractArg]] = None,
        expect: Optional[list[AbstractExpectedResult]] = None,
    ) -> None:
        self.stdout = ""
        self.stderr = ""
        self.code: Optional[int] = None
        self.command = command
        self.arguments: list[AbstractArg] = arguments or []
        self.expect: list[AbstractExpectedResult] = expect or [
            NoStdErr(),
            SuccessCode(),
        ]

    def join(self) -> str:
        return f"{self.command} {' '.join(arg.fmt_str() for arg in self.arguments)}"

    def build(self) -> list[str]:
        return [self.command, *sum((arg.fmt_list() for arg in self.arguments), [])]

    def execute(self, shell: bool = False) -> None:
        command = self.build()
        process = subprocess.run(command, capture_output=True, text=True, shell=shell)
        self.stdout = process.stdout
        self.stderr = process.stderr
        self.code = process.returncode

    def check(self) -> bool:
        results = tuple(awaited.check(self) for awaited in self.expect)
        if all(results):
            return True
        else:
            false_checks = tuple(
                expect_obj
                for expect_obj, res in zip(self.expect, results)
                if res is False
            )
            raise UnexpectedResultError(f"Unexpected results:\n{false_checks}")

    def arg_values(self) -> list[Any]:
        return [self.command, *sum((arg.arg_values() for arg in self.arguments), [])]
