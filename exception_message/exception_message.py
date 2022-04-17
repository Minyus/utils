import sys
import traceback


def _get_exception_msg():
    return "".join(traceback.format_exception(*sys.exc_info()))


if __name__ == "__main__":
    try:
        foo = 1 / 0
    except Exception:
        msg = _get_exception_msg()
        print(
            "\n".join(
                [
                    "The following exception occurred!",
                    "-" * 50,
                    msg,
                    "-" * 50,
                    "Continue running the code without interruption...",
                ]
            )
        )
