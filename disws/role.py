"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

from typing import Optional, Self, Dict, Any

from disws.types import Role as MsgRole, RoleTags
from disws.utils import get_role_icon_url


class Role:
    __slots__ = (
        "id",
        "name",
        "color",
        "hoist",
        "icon",
        "unicode_emoji",
        "position",
        "permissions",
        "managed",
        "mentionable",
        "tags",
    )

    def __init__(self, data: MsgRole) -> None:
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self.color: int = data.get("color", 0)
        self.hoist: bool = data.get("hoist", False)
        self.icon: Optional[str] = data.get("icon", None)
        self.unicode_emoji: Optional[str] = data.get("unicode_emoji", None)
        self.position: int = int(data["position"])
        self.permissions: Optional[int] = (
            int(data["permissions"]) if data.get("permissions", None) else None
        )
        self.managed: bool = data.get("managed", False)
        self.mentionable: bool = data.get("mentionable", False)
        self.tags: Optional[RoleTags] = data.get("tags", None)

    def __repr__(self) -> str:
        return f"<role={self.name!r}, id={self.id}, color={self.color!r}>"

    def __str__(self) -> str:
        return self.name

    def icon_url(self) -> Optional[str]:
        return get_role_icon_url(self.id, self.icon)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "hoist": self.hoist,
            "icon": self.icon,
            "unicode_emoji": self.unicode_emoji,
            "position": self.position,
            "permissions": self.permissions,
            "managed": self.managed,
            "mentionable": self.mentionable,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(data=data)
