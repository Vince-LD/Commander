from typing import Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")


class CommandArg(ABC, Generic[T]):
    @abstractmethod
    def arg_values(self) -> list[T]:
        ...

    @abstractmethod
    def fmt_list(self) -> list[str]:
        ...

    @abstractmethod
    def fmt_str(self) -> str:
        ...


class PositionalArgs(CommandArg, Generic[T]):
    def __init__(self, *args: T) -> None:
        self.args = args

    def fmt_list(self) -> list[str]:
        return [str(arg) for arg in self.args]

    def fmt_str(self) -> str:
        return " ".join(self.fmt_list())

    def arg_values(self) -> list[T]:
        return list(self.args)


class SimpleNamedArgument(CommandArg, Generic[T]):
    def __init__(self, name: str, value: T) -> None:
        self.name = name if name.startswith("-") else f"--{name}"
        self.value = value

    def fmt_list(self) -> list[str]:
        return [f"{self.name}", str(self.value)]

    def fmt_str(self) -> str:
        return " ".join(self.fmt_list())

    def arg_values(self) -> list[str | T]:
        return [self.name, self.value]


class ListNamedArgument(CommandArg, Generic[T]):
    def __init__(self, name: str, value: list[T]) -> None:
        self.name = name if name.startswith("-") else f"--{name}"
        self.value = value

    def fmt_list(self) -> list[str]:
        return [f"{self.name}", *map(str, self.value)]

    def fmt_str(self) -> str:
        return " ".join(self.fmt_list())

    def arg_values(self) -> list[str | T]:
        return [self.name, *self.value]


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

    def arg_values(self) -> list[str | T]:
        return [self.name, *self.value]


class ConditionalArg(CommandArg, Generic[T]):
    def __init__(self, condition: bool, arg: CommandArg[T]) -> None:
        self.condition = condition
        self.arg = arg

    def fmt_list(self) -> list[str]:
        return self.arg.fmt_list() if self.condition else []

    def fmt_str(self) -> str:
        return self.arg.fmt_str() if self.condition else ""

    def arg_values(self) -> list[T]:
        return self.arg.arg_values()
