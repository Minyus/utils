import subprocess
import time


def get_lines(cmd, **kwargs):
    proc = subprocess.Popen(
        cmd,
        shell=not isinstance(cmd, list),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        **kwargs
    )
    while True:
        line = proc.stdout.readline()
        if line:
            yield line.decode()
        else:
            if proc.poll() is None:
                time.sleep(0.1)
            else:
                break


def run(cmd, show=True, **kwargs):
    for text in get_lines(cmd, **kwargs):
        if show:
            print(text, end="")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Realtime subprocess.")
    parser.add_argument(
        "-c",
        "--cmd",
        type=str,
        help="The command to run.",
        default="echo Started to run demo;sleep 0.5;echo 1;sleep 0.5;echo 2;sleep 0.5;echo 3;sleep 0.5;echo Finished",
    )

    args = parser.parse_args()

    def generate_cmd(args):
        return args.cmd

    cmd = generate_cmd(args)
    run(cmd)
