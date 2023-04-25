"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

from typing import Any, List, Optional, Self, Union, Dict

from disws.types import Guild as MsgGuild, GuildWelcomeScreen
from disws.utils import get_guild_banner_url, get_guild_icon_url, get_guild_splash_url
from .emoji import Emoji
from .role import Role
from .user import Member


class Guild:
    __slots__ = (
        "id",
        "name",
        "unavailable",
        "icon",
        "icon_hash",
        "splash",
        "discovery_splash",
        "user_is_owner",
        "owner_id",
        "owner",
        "permissions",
        "afk_channel_id",
        "afk_timeout",
        "widget_enabled",
        "widget_channel_id",
        "verification_level",
        "default_message_notifications",
        "explicit_content_filter",
        "roles",
        "emojis",
        "mfa_level",
        "application_id",
        "system_channel_id",
        "system_channel_flags",
        "rules_channel_id",
        "max_presences",
        "max_members",
        "vanity_url_code",
        "description",
        "banner",
        "premium_tier",
        "premium_subscription_count",
        "preferred_locale",
        "public_updates_channel_id",
        "max_video_channel_users",
        "approximate_member_count",
        "approximate_presence_count",
        "welcome_screen",
        "nsfw_level",
        "stickers",
        "premium_progress_bar_enabled",
    )

    def __init__(self, data: MsgGuild) -> None:
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self.unavailable: bool = data.get("unavailable", False)
        self.icon: Optional[str] = data.get("icon", None)
        self.icon_hash: Optional[str] = data.get("icon_hash", None)
        self.splash: Optional[str] = data.get("splash", None)
        self.discovery_splash: Optional[str] = data.get("discovery_splash", None)
        self.user_is_owner: bool = data.get("user_is_owner", False)
        self.owner_id: int = int(data["owner_id"])
        self.owner: Optional[Member] = Member(data.get("owner_data", None))
        self.permissions: int = (
            int(data["permissions"]) if data.get("permissions", None) else 0
        )
        self.afk_channel_id: Optional[int] = (
            int(data["afk_channel_id"]) if data.get("afk_channel_id", None) else None
        )
        self.afk_timeout: Optional[int] = (
            int(data["afk_timeout"]) if data.get("afk_timeout", None) else None
        )
        self.widget_enabled: bool = data.get("widget_enabled", False)
        self.widget_channel_id: Optional[int] = (
            int(data["widget_channel_id"])
            if data.get("widget_channel_id", None)
            else None
        )
        self.verification_level: int = int(data["verification_level"])
        self.default_message_notifications: int = int(
            data["default_message_notifications"]
        )
        self.explicit_content_filter: Optional[int] = (
            int(data["explicit_content_filter"])
            if data.get("explicit_content_filter", None)
            else None
        )
        self.roles: Union[List[Role]] = (
            [Role(role) for role in data.get("roles", [])]
            if data.get("roles", [])
            else []
        )
        self.emojis: Union[List[Emoji]] = (
            [Emoji(emoji) for emoji in data.get("emojis", [])]
            if data.get("emojis", [])
            else []
        )
        self.mfa_level: int = int(data["mfa_level"])
        self.application_id: Optional[int] = (
            int(data["application_id"]) if data.get("application_id", None) else None
        )
        self.system_channel_id: Optional[int] = (
            int(data["system_channel_id"])
            if data.get("system_channel_id", None)
            else None
        )
        self.system_channel_flags: Optional[int] = (
            int(data["system_channel_flags"])
            if data.get("system_channel_flags", None)
            else None
        )
        self.rules_channel_id: Optional[int] = (
            int(data["rules_channel_id"])
            if data.get("rules_channel_id", None)
            else None
        )
        self.max_presences: Optional[int] = (
            int(data["max_presences"]) if data.get("max_presences", None) else None
        )
        self.max_members: Optional[int] = (
            int(data["max_members"]) if data.get("max_members", None) else None
        )
        self.vanity_url_code: Optional[str] = data.get("vanity_url_code", None)
        self.description: Optional[str] = data.get("description", None)
        self.banner: Optional[str] = data.get("banner", None)
        self.premium_tier: int = int(data["premium_tier"])
        self.premium_subscription_count: int = int(data["premium_subscription_count"])
        self.preferred_locale: Optional[str] = data.get("preferred_locale", None)
        self.public_updates_channel_id: Optional[int] = (
            int(data["public_updates_channel_id"])
            if data.get("public_updates_channel_id", None)
            else None
        )
        self.max_video_channel_users: Optional[int] = (
            int(data["max_video_channel_users"])
            if data.get("max_video_channel_users", None)
            else None
        )
        self.approximate_member_count: Optional[int] = (
            int(data["approximate_member_count"])
            if data.get("approximate_member_count", None)
            else None
        )
        self.approximate_presence_count: Optional[int] = (
            int(data["approximate_presence_count"])
            if data.get("approximate_presence_count", None)
            else None
        )
        self.welcome_screen: Optional[GuildWelcomeScreen] = data.get(
            "welcome_screen", None
        )
        self.nsfw_level: int = int(data["nsfw_level"])
        self.stickers: List[Any] = data.get("stickers", [])
        self.premium_progress_bar_enabled: bool = data.get(
            "premium_progress_bar_enabled", False
        )

    def icon_url(self) -> Optional[str]:
        """Get the icon url of this guild."""
        return get_guild_icon_url(self.id, self.icon)

    def banner_url(self) -> Optional[str]:
        """Get the banner url of this guild."""
        return get_guild_banner_url(self.id, self.banner)

    def splash_url(self) -> Optional[str]:
        """Get the splash url of this guild."""
        return get_guild_splash_url(self.id, self.splash)

    def __repr__(self) -> Optional[str]:
        return f"<Guild id={self.id} name={self.name}>"

    def __str__(self) -> Optional[str]:
        return f"{self.name} ({self.id})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "unavailable": self.unavailable,
            "icon": self.icon,
            "icon_hash": self.icon_hash,
            "splash": self.splash,
            "discovery_splash": self.discovery_splash,
            "user_is_owner": self.user_is_owner,
            "owner_id": self.owner_id,
            "owner": self.owner.to_dict() if self.owner else None,
            "permissions": self.permissions,
            "afk_channel_id": self.afk_channel_id,
            "afk_timeout": self.afk_timeout,
            "widget_enabled": self.widget_enabled,
            "widget_channel_id": self.widget_channel_id,
            "verification_level": self.verification_level,
            "default_message_notifications": self.default_message_notifications,
            "explicit_content_filter": self.explicit_content_filter,
            "roles": [role.to_dict() for role in self.roles] if self.roles else [],
            "emojis": [emoji.to_dict() for emoji in self.emojis] if self.emojis else [],
            "mfa_level": self.mfa_level,
            "application_id": self.application_id,
            "system_channel_id": self.system_channel_id,
            "system_channel_flags": self.system_channel_flags,
            "rules_channel_id": self.rules_channel_id,
            "max_presences": self.max_presences,
            "max_members": self.max_members,
            "vanity_url_code": self.vanity_url_code,
            "description": self.description,
            "banner": self.banner,
            "premium_tier": self.premium_tier,
            "premium_subscription_count": self.premium_subscription_count,
            "preferred_locale": self.preferred_locale,
            "public_updates_channel_id": self.public_updates_channel_id,
            "max_video_channel_users": self.max_video_channel_users,
            "approximate_member_count": self.approximate_member_count,
            "approximate_presence_count": self.approximate_presence_count,
            "welcome_screen": self.welcome_screen,
            "nsfw_level": self.nsfw_level,
            "stickers": self.stickers,
            "premium_progress_bar_enabled": self.premium_progress_bar_enabled,
        }

    @classmethod
    def from_dict(cls, data: Dict[Any, Any]) -> Self:
        return cls(data=data)


class GuildCache:
    guilds: Dict[str, Union[Dict[Any, Any], Guild]] = {}

    def __init__(self) -> None:
        pass

    def __repr__(self) -> Optional[str]:
        return f"<GuildCache: {len(self.guilds)} guilds>"

    def __str__(self) -> Optional[str]:
        return f"{len(self.guilds)} guilds"

    def __get_guild(self, guild_id: str) -> Optional[Union[Dict[Any, Any], Guild]]:
        return self.guilds.get(guild_id, None)

    def try_get(self, guild_id: str) -> Optional[Union[Dict[Any, Any], Guild]]:
        return self.__get_guild(guild_id)

    def add_guild(
        self, guild_id: str, guild: Union[Dict[Any, Any], Guild]
    ) -> Union[Dict[Any, Any], Guild]:
        self.guilds[guild_id] = guild
        return guild

    def remove_guild(self, guild_id: str) -> None:
        del self.guilds[guild_id]

    def clear(self) -> None:
        return self.guilds.clear()
