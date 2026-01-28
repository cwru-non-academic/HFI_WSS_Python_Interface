class WssLoader:
    def __init__(self, dll_path: str) -> None:
        self.dll_path = dll_path

    def load(self) -> None:
        """Load the WSS interface DLL via pythonnet."""
        raise NotImplementedError("Wire up pythonnet load logic here.")
