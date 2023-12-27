class APIException(Exception):
    """Base Exception"""

    @property
    def message(self) -> str:
        return "An API error occurred"
