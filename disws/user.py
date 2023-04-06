"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

from typing import Any, Dict, List, Optional, Union

import disws.guild
from disws.utils import (
    from_iso_format_to_humanly, get_avatar_url, get_banner_url, get_flag,
    get_member_create_date,
    guild_member_avatar_url
)
from .role import Role
from .types import User, UserTag


class BaseUser(UserTag):
    __slots__ = (
        "name", "id", "discriminator", "avatar",
        "avatar_decoration", "banner", "accent_color",
        "bot", "system", "public_flags",
    )

    def __init__(self, data: User) -> None:
        self._update(data)

    def _update(self, data: User) -> None:
        self.name: Optional[str] = data.get("username", None)
        self.id: int = int(data.get("id", 0))
        self.discriminator: Optional[str] = data.get("discriminator", None)
        self.avatar: Optional[str] = get_avatar_url(self.id, data["avatar"]) if data.get("avatar", None) else None
        self.avatar_decoration: Optional[str] = data.get("avatar_decoration", None)
        self.banner: Optional[str] = (
            get_banner_url(self.id, data["banner"])
            if data.get("banner", None)
            else None
        )
        self.accent_color: Optional[int] = data.get("accent_color", None)
        self.public_flags: Optional[int] = data.get("public_flags", 0)
        self.bot: bool = data.get("bot", False)
        self.system: bool = data.get("system", False)

    @property
    def created_at(self) -> Optional[str]:
        return get_member_create_date(self.id)

    @property
    def display_name(self) -> Optional[str]:
        return self.name


class Me(BaseUser):
    __slots__ = (
        "locale", "flags", "verified", "mfa_enabled",
        "email", "phone", "premium_type", "bio",
        "nsfw_allowed", "purchased_flags", "premium_usage_flags",
    )

    def __init__(self, data: User) -> None:
        super().__init__(data)
        self._full_update(data)

    def __repr__(self) -> str:
        return f"<id={self.id}, name={self.name!r}, discriminator={self.discriminator!r} locale={self.locale}>"

    def __str__(self) -> str:
        return f"{self.name}#{self.discriminator}"

    def _full_update(self, data: User) -> None:
        self._update(data)
        self.verified: bool = data.get("verified", False)
        self.email: Optional[str] = data.get("email", None)
        self.phone: Optional[str] = data.get("phone", None)
        self.locale: Optional[str] = data.get("locale", "en-US")
        self.flags: Optional[int] = data.get("flags", 0)
        self.purchased_flags: Optional[int] = data.get("purchased_flags", 0)
        self.premium_usage_flags: Optional[int] = data.get("premium_usage_flags", 0)
        self.mfa_enabled: bool = data.get("mfa_enabled", False)
        self.premium_type: Optional[str] = get_flag(data["premium_type"]) if data.get("premium_type", None) else None
        self.bio: Optional[str] = data.get("bio", None)
        self.nsfw_allowed: bool = data.get("nsfw_allowed", False)

    @property
    def full_name(self) -> str:
        return f"{self.name}#{self.discriminator}"

    def to_dict(self) -> Dict[str, Union[Optional[str], Optional[int], Optional[bool]]]:
        return {
            "id": self.id,
            "username": self.name,
            "discriminator": self.discriminator,
            "created_at": self.created_at,
            "avatar": self.avatar,
            "avatar_decoration": self.avatar_decoration,
            "banner": self.banner,
            "accent_color": self.accent_color,
            "bot": self.bot,
            "system": self.system,
            "public_flags": self.public_flags,
            "verified": self.verified,
            "mfa_enabled": self.mfa_enabled,
            "email": self.email,
            "phone": self.phone,
            "locale": self.locale,
            "flags": self.flags,
            "purchased_flags": self.purchased_flags,
            "premium_usage_flags": self.premium_usage_flags,
            "premium_type": self.premium_type,
            "bio": self.bio,
            "nsfw_allowed": self.nsfw_allowed,
        }


class Member(BaseUser):
    __slots__ = (
        "guild", "nick", "guild_avatar", "roles",
        "joined_at", "premium_since", "deaf", "mute",
        "guild_flags", "pending", "guild_permissions", "timeout",
    )

    def __init__(self, data: User, guild: Any = None) -> None:
        super().__init__(data)
        self._update(data)
        self._guild_update(guild)

    def _guild_update(
        self,
        data: Dict[Any, Any] = Optional[Dict[Any, Any]],
    ) -> None:
        if data is not None:
            self.guild: Optional[disws.guild.Guild] = disws.guild.Guild(data["guild"]) if data.get("guild",
                                                                                                   None) else None
            self.nick: Optional[str] = data.get("nick", None)
            self.guild_avatar: Optional[str] = guild_member_avatar_url(
                self.guild.id, self.id, data["avatar"]
            ) if data.get("avatar", None) and data.get("guild", None) else None
            self.roles: List[Role] = self._get_roles(data.get("roles")) if data.get("roles", None) else []
            self.premium_since: Optional[str] = from_iso_format_to_humanly(
                data["premium_since"]
            ) if data.get("premium_since", None) else None
            self.deaf: bool = data.get("deaf", False)
            self.mute: bool = data.get("mute", False)
            self.guild_flags: int = data.get("guild_flags", 0)
            self.pending: bool = data.get("pending", False)
            self.guild_permissions: int = data.get("guild_permissions", 0)
            self.timeout: Optional[str] = from_iso_format_to_humanly(
                data["communication_disabled_until"]
            ) if data.get("communication_disabled_until", None) else None

    def _get_roles(self, data: List["Role"]) -> List["Role"]:
        if getattr(self, "guild_id", None):
            return [role for role in self.guild.roles if str(role.id) in data]

    def __repr__(self) -> str:
        return (
            f"<id={self.id}, name={self.name!r}, discriminator={self.discriminator!r}, created_at={self.created_at}>"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.name,
            "discriminator": self.discriminator,
            "created_at": self.created_at,
            "avatar": self.avatar,
            "avatar_decoration": self.avatar_decoration,
            "banner": self.banner,
            "accent_color": self.accent_color,
            "bot": self.bot,
            "system": self.system,
            "public_flags": self.public_flags,
            "guild": self.guild.to_dict() if getattr(self, "guild", None) else None,
            "nick": self.nick if getattr(self, "nick", None) else None,
            "guild_avatar": self.guild_avatar if getattr(self, "guild_avatar", None) else None,
            "roles": self.roles if getattr(self, "roles", None) else [],
            "joined_at": self.joined_at if getattr(self, "joined_at", None) else None,
            "premium_since": self.premium_since if getattr(self, "premium_since", None) else None,
            "deaf": self.deaf if getattr(self, "deaf", None) else False,
            "mute": self.mute if getattr(self, "mute", None) else False,
            "guild_flags": self.guild_flags if getattr(self, "guild_flags", None) else 0,
            "pending": self.pending if getattr(self, "pending", None) else False,
            "guild_permissions": self.guild_permissions if getattr(self, "guild_permissions", None) else False,
            "timeout": self.timeout if getattr(self, "timeout", None) else None,
        }
