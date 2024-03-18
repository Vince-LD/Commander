from typing import Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")


class CommandArg(ABC, Generic[T]):
    @abstractmethod
    def fmt_list(self) -> list[str]:
        ...

    @abstractmethod
    def fmt_str(self) -> str:
        ...


class PositionalArg(CommandArg, Generic[T]):
    def __init__(self, *args: T) -> None:
        self.value = args

    def fmt_list(self) -> list[str]:
        return [str(arg) for arg in self.value]

    def fmt_str(self) -> str:
        return " ".join(self.fmt_list())


class SimpleNamedArgument(CommandArg, Generic[T]):
    def __init__(self, name: str, value: T) -> None:
        self.name = name if name.startswith("-") else f"--{name}"
        self.value = value

    def fmt_list(self) -> list[str]:
        return [f"{self.name}", str(self.value)]

    def fmt_str(self) -> str:
        return " ".join(self.fmt_list())


class ListNamedArgument(CommandArg, Generic[T]):
    def __init__(self, name: str, value: list[T]) -> None:
        self.name = name if name.startswith("-") else f"--{name}"
        self.value = value

    def fmt_list(self) -> list[str]:
        return [f"{self.name}", *map(str, self.value)]

    def fmt_str(self) -> str:
        return " ".join(self.fmt_list())


class RepeatableNamedArg(CommandArg, Generic[T]):
    def __init__(self, name: str, value: list[T]) -> None:
        self.name = name if name.startswith("-") else f"--{name}"
        self.value = value

    def fmt_list(self) -> list[str]:
        arg_list = []
        for arg in map(str, self.value):
            arg_list.extend((self.name, arg))
        return arg_list

    def fmt_str(self) -> str:
        return " ".join(self.fmt_list())


class ConditionalArg(CommandArg, Generic[T]):
    def __init__(self, condition: bool, arg: CommandArg[T]) -> None:
        self.condition = condition
        self.arg = arg

    def fmt_list(self) -> list[str]:
        return self.arg.fmt_list() if self.condition else []

    def fmt_str(self) -> str:
        return self.arg.fmt_str() if self.condition else ""
