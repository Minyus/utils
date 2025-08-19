class DefaultList(list):
    def __init__(self, default_value, *args):
        super().__init__(*args)
        self.default_value = default_value

    def __getitem__(self, index):
        if index >= len(self) or index < -len(self):
            return self.default_value
        return super().__getitem__(index)


# Example usage
default_list = DefaultList(0, [1, 2, 3])
print(default_list[1])  # Output: 2
print(default_list[5])  # Output: 0 (default value)
