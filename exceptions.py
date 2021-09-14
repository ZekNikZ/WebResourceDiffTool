class MissingSettingsError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class LoaderError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class CustomConnectionError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)