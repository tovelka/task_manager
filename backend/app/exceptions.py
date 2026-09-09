class NotFoundException(Exception):
    status_code = 404

    def __init__(self, details: str, *args: object) -> None:
        self.details = details
        super().__init__(*args)


class AccessDeniedException(Exception):
    status_code = 403

    def __init__(self, details: str, *args: object) -> None:
        self.details = details
        super().__init__(*args)


class DuplicateException(Exception):
    status_code = 409

    def __init__(self, details: str, *args: object) -> None:
        self.details = details
        super().__init__(*args)


class UncorrectDataException(Exception):
    status_code = 422

    def __init__(self, details: str, *args: object) -> None:
        self.details = details
        super().__init__(*args)
