"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

from typing import List, Optional, Self, Dict, Any

from disws.types import Emoji as MsgEmoji
from .role import Role
from .user import Member


class Emoji:
    __slots__ = ("id", "name", "roles", "user", "require_colons", "managed", "animated", "available")

    def __init__(self, data: MsgEmoji):
        self.id: int = int(data["id"])
        self.name: Optional[str] = data.get("name", None)
        self.roles: Optional[List[Role]] = data.get("roles", None)
        self.user: Optional[Member] = Member(data["user"]) if data.get("user", None) else None
        self.require_colons: bool = data.get("require_colons", False)
        self.managed: bool = data.get("managed", False)
        self.animated: bool = data.get("animated", False)
        self.available: bool = data.get("available", False)

    def __repr__(self) -> str:
        return f"<emoji={self.name!r}, id={self.id}, roles={self.roles!r}>"

    def __str__(self) -> str:
        return self.name or "Unknown"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "roles": [role.to_dict() for role in self.roles if isinstance(role, Role)] if self.roles else None,
            "user": self.user.to_dict() if self.user else None,
            "require_colons": self.require_colons,
            "managed": self.managed,
            "animated": self.animated,
            "available": self.available,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(data=data)
