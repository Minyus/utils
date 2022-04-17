import subprocess
import os

from pyarrow import fs
from fsspec.implementations.arrow import ArrowFSWrapper

os.environ["CLASSPATH"] = subprocess.run(
    "hadoop classpath --glob", shell=True, capture_output=True
).stdout.decode()

hdfs = ArrowFSWrapper(fs.HadoopFileSystem("default"))

if __name__ == "__main__":

    hdfs.ls("/hdfs_dir/")

    hdfs.glob("/hdfs_dir/*.txt")

    with hdfs.open("hdfs_dir/foo.txt", "w") as f:
        f.write("some contents")

    hdfs.cat("hdfs_dir/foo.txt").decode()
