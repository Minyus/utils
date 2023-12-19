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
