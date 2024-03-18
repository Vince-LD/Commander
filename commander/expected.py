from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
    from commander.command import Command


class ExpectedResult(ABC):
    @abstractmethod
    def check(self, result: "Command") -> bool:
        ...


class ExpectedStdout(ExpectedResult):
    def __init__(self, stdout: str) -> None:
        self.stdout = stdout

    def check(self, result: "Command") -> bool:
        return self.stdout in result.stdout


class NoStdErr(ExpectedResult):
    def check(self, result: "Command") -> bool:
        return result.stderr == ""


class SuccessCode(ExpectedResult):
    def check(self, result: "Command") -> bool:
        return result.code == 0


class ExpectCode(ExpectedResult):
    def __init__(self, code: int) -> None:
        self.code = code

    def check(self, result: "Command") -> bool:
        return result.code == self.code


class FilesExist(ExpectedResult):
    def __init__(self, *files: str) -> None:
        self.files = files

    def check(self, result: "Command") -> bool:
        return all(os.path.isfile(file) for file in self.files)
