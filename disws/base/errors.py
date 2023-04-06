"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""


class DiscordException(Exception):
    """Raised when a Discord API request fails."""

    def __init__(self, *, status_code: int, text: str) -> None:
        super().__init__(f"\nStatus code -> {status_code}\nText -> {text}")


class HTTPException(DiscordException):
    """Raised when an HTTP request fails."""

    def __init__(self, *, status_code: int, text: str) -> None:
        super().__init__(status_code=status_code, text=text)


class DiscordTokenError(DiscordException):
    """Raised when the token is invalid."""

    def __init__(self, *, status_code: int = 401, text: str) -> None:
        super().__init__(status_code=status_code, text=text)
