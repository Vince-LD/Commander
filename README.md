# Commander

Simple command line utils integrated in the [Tuyaux](https://github.com/Vince-LD/tuyaux) library.

The goal of this library is to use standard interfaces to assemble commande lines more easily than doing it manually everytime. The goal is also to provide standard classes to check your command results.

Basic examples can be found [here](examples/basic.py) and below:

```python
cmd = Command("cp")
cmd.add_arguments(PositionalArgs("src/path/first.txt", "src/path/second.txt", "dest/path/"))
cmd.add_expectations(
        NoStdErr(),
        SuccessCode(),
        FilesExist("dest/path/first.txt", "dest/path/second.txt"),
)
assert cmd.join() == "cp src/path/first.txt src/path/second.txt dest/path/"
```

```python
cmd = Command("ls")
cmd.add_arguments(
    PositionalArgs("dest/path/"),
    FlagArgs("--all", "-R"),
) 
cmd.add_expectations(
        SuccessCode(), 
        StdoutContains("inner/dir")
)
assert cmd.join() == "ls --all -R dest/path/"
```

```python
# Other syntax using the constructor
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