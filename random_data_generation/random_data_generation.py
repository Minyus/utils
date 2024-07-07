from pathlib import Path
import numpy

dir = "/Volumes/SanDisk/random_dummy"


import numpy as np


def generate_random_bytes_and_write_to_file(file_path, num_bytes):
    """
    Generates a specified number of random bytes and writes them to a file.

    Parameters:
    - file_path: Path to the output file.
    - num_bytes: Number of random bytes to generate.
    """
    # Generate random bytes
    random_bytes = np.random.bytes(num_bytes)

    # Write the bytes to the file
    with open(file_path, "wb") as file:
        file.write(random_bytes)


# Example usage
file_path = "random_bytes.bin"
num_bytes = 1000  # Specify the number of bytes you want to generate
generate_random_bytes_and_write_to_file(file_path, num_bytes)

digits = 11
for e in range(digits):
    num_bytes = 10**e
    for i in range(10):
        generate_random_bytes_and_write_to_file(dir + f"/1e+{e:02d}_{i}", num_bytes)
