import subprocess
from typing import Any, Iterable, Optional
from commander.expected import AbstractExpectedResult, NoStdErr, SuccessCode
from commander.arguments import AbstractArg
from commander.exceptions import CommandNotExecuted, UnexpectedResultError


class Command:
    def __init__(
        self,
        command: str,
        arguments: Optional[Iterable[AbstractArg]] = None,
        expect: Optional[Iterable[AbstractExpectedResult]] = None,
    ) -> None:
        self.stdout = ""
        self.stderr = ""
        self.code: Optional[int] = None
        self.command = command
        self.arguments: list[AbstractArg] = (
            list(arguments) if arguments is not None else []
        )
        self.expect: list[AbstractExpectedResult] = (
            list(expect)
            if expect is not None
            else [
                NoStdErr(),
                SuccessCode(),
            ]
        )
        self._executed = False

    def add_arguments(self, *args: AbstractArg):
        self.arguments.extend(args)

    def add_expectations(self, *args: AbstractExpectedResult):
        self.expect.extend(args)

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
        self._executed = True

    def check(self) -> bool:
        if not self._executed:
            raise CommandNotExecuted(
                "Command should be executed before checking its results."
                "Call Command.execute() before Command.check() to fix this error."
            )
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
