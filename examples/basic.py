from commander.command import Command
from commander.arguments import (
    FlagArgs,
    SimpleNamedArg,
    PositionalArgs,
)
from commander.expected import FilesExist, NoStdErr, SuccessCode, StdoutContains


def copy_file_example():
    cmd = Command(
        command="cp",
        arguments=[
            PositionalArgs("src/path/first.txt", "src/path/second.txt", "dest/path/")
        ],
        expect=[
            NoStdErr(),
            SuccessCode(),
            FilesExist("dest/path/first.txt", "dest/path/second.txt"),
        ],
    )
    print(cmd.build())
    assert cmd.join() == "cp src/path/first.txt src/path/second.txt dest/path/"


def list_files():
    cmd = Command(
        command="ls",
        arguments=[FlagArgs("--all", "-R"), PositionalArgs("dest/path/")],
        expect=[SuccessCode(), StdoutContains("inner/dir")],
    )
    print(cmd.build())
    assert cmd.join() == "ls --all -R dest/path/"


def grep_text_files():
    cmd = Command(
        command="grep",
        arguments=[
            SimpleNamedArg("-rin", '"pattern"'),
            SimpleNamedArg("--include", '"*.txt"'),
            PositionalArgs("search/path/"),
        ],
    )
    print(cmd.build())
    assert cmd.join() == 'grep -rin "pattern" --include "*.txt" search/path/'


if __name__ == "__main__":
    copy_file_example()
    list_files()
    grep_text_files()
