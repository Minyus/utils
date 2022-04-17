from fsspec.implementations.local import LocalFileSystem

local = LocalFileSystem()

if __name__ == "__main__":

    local.ls("/local_dir/")

    local.glob("/local_dir/*.txt")

    with local.open("/local_dir/foo.txt", "w") as f:
        f.write("some contents")

    local.cat("/local_dir/foo.txt").decode()
