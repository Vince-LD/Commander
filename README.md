# Commander

Simple command line utils integrated in the [Tuyaux](https://github.com/Vince-LD/tuyaux) library.

The goal of this library is to use standard interfaces to assemble commande lines more easily than doing it manually everytime. The goal is also to provide standard classes to check your command results.

Basic examples can be found [here](examples/basic.py) and below:

```python
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
assert cmd.join() == "cp src/path/first.txt src/path/second.txt dest/path/"
```

```python
cmd = Command(
    command="ls",
    arguments=[
        lagArgs("--all", "-R"), 
        PositionalArgs("dest/path/")],
    expect=[
        SuccessCode(), 
        StdoutContains("inner/dir")
        ],
)
assert cmd.join() == "ls --all -R dest/path/"
```

```python
cmd = Command(
        command="grep",
        arguments=[
            SimpleNamedArg("-rin", '"pattern"'),
            SimpleNamedArg("--include", '"*.txt"'),
            PositionalArgs("search/path/"),
        ],
    )
assert cmd.join() == 'grep -rin "pattern" --include "*.txt" search/path/'
```