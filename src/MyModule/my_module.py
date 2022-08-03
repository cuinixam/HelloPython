from pathlib import Path


class MyModule:
    def __init__(self, file: Path):
        self.file = file

    def read(self) -> str:
        return self.file.read_text()
