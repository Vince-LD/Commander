from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
    from commander.command import Command


class AbstractExpectedResult(ABC):
    @abstractmethod
    def check(self, result: "Command") -> bool:
        ...


class ExpectedStdout(AbstractExpectedResult):
    def __init__(self, stdout: str) -> None:
        self.stdout = stdout

    def check(self, result: "Command") -> bool:
        return self.stdout in result.stdout


class NoStdErr(AbstractExpectedResult):
    def check(self, result: "Command") -> bool:
        return result.stderr == ""


class SuccessCode(AbstractExpectedResult):
    def check(self, result: "Command") -> bool:
        return result.code == 0


class ExpectCode(AbstractExpectedResult):
    def __init__(self, code: int) -> None:
        self.code = code

    def check(self, result: "Command") -> bool:
        return result.code == self.code


class PathsExist(AbstractExpectedResult):
    def __init__(self, *paths: str) -> None:
        self.paths = paths

    def check(self, result: "Command") -> bool:
        return all(os.path.isfile(path) for path in self.paths)


class FilesExist(AbstractExpectedResult):
    def __init__(self, *files: str) -> None:
        self.files = files

    def check(self, result: "Command") -> bool:
        return all(os.path.isfile(file) for file in self.files)
