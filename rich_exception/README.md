# Rich Exception

Python developers use print(variable_foobar) or debugging feature of IDE such as VS Code to troubleshoot, but aren't there any quicker alternative ways?

`rich` package can make the exception traceback nicer; show the local variable values and extra lines of code.

## How to use

1. Install rich

```bash
pip install -U rich
```

2. Place the following code in the beginning of your main module.

```python
try:
    from rich.traceback import install

    install(
        console=None,
        width=200,
        extra_lines=3,
        theme=None,
        word_wrap=True,
        show_locals=True,
        locals_max_length=10,
        locals_max_string=80,
        locals_hide_dunder=True,
        locals_hide_sunder=None,
        indent_guides=True,
        suppress=(),
        max_frames=20,
    )
except Exception:
    print("Failed to set up rich traceback. Try: pip install -U rich")
```

Alternatively, to apply to all the codes you run, you may place the Python code in `sitecustomize.py` file in `site-packages` directory which can be found by running:

```bash
python -c "import sys;print(sys.path)"
```

## References

Regarding the options, see the documents:

<https://rich.readthedocs.io/en/stable/traceback.html#traceback-handler>
<https://rich.readthedocs.io/en/stable/reference/traceback.html#rich.traceback.install>
