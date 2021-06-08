class APIError(Exception):
    """Raised when there is an error communicating with the API."""

    def __init__(self, status_code: int):
        self.status_code = status_code

    def __repr__(self):
        return f"There was an issue communicating with the API! Response Code: {self.status_code}"
