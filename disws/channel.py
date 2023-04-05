"""
discord-websocket (disws, ver 0.0.6)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

from typing import Any, Dict, List, Literal, Optional, Self, Union

from disws.types import (
    PermissionOverwrite, Snowflake, TextChannel as MsgTextChannel, ThreadArchiveDuration,
    VideoQualityMode,
    VoiceChannel as MsgVoiceChannel
)
from .guild import Guild


class TextChannel:
    __slots__ = (
        "id", "name", "guild", "guild_id", "position", "permission_overwrites",
        "nsfw", "guild", "parent_id", "topic", "last_message_id", "last_pin_timestamp",
        "rate_limit_per_user", "default_auto_archive_duration", "type",
    )

    def __init__(self, data: MsgTextChannel) -> None:
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self.guild_id: int = int(data["guild_id"])
        self.guild: Optional[Guild] = Guild(data["guild"]) if data["guild"] else None
        self.position: int = data.get("position", 0)
        self.permission_overwrites: List[PermissionOverwrite] = data.get("permission_overwrites", [])
        self.nsfw: bool = data.get("nsfw", False)
        self.parent_id: Union[Optional[str], Optional[int]] = data.get("parent_id", None)
        self.topic: Optional[str] = data.get("topic", None)
        self.last_message_id: Union[str, Optional[int]] = data.get("last_message_id", None)
        self.last_pin_timestamp: Optional[str] = data.get("last_pin_timestamp", None)
        self.rate_limit_per_user: int = data.get("rate_limit_per_user", 0)
        self.default_auto_archive_duration: Optional[
            ThreadArchiveDuration
        ] = data.get("default_auto_archive_duration", None)
        self.type: Literal[0] = data.get("type", 0)

    def __repr__(self) -> str:
        return f"<TextChannel id={self.id} name={self.name!r}>"

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "guild_id": self.guild_id,
            "position": self.position,
            "topic": self.topic,
            "nsfw": self.nsfw,
            "last_message_id": self.last_message_id,
            "rate_limit_per_user": self.rate_limit_per_user,
        }

    @classmethod
    def from_dict(cls, data: Dict[Any, Any]) -> Self:
        return cls(data)


class VoiceChannel:
    __slots__ = (
        "id", "name", "guild_id", "position", "permission_overwrites", "parent_id",
        "topic", "last_message_id", "last_pin_timestamp", "rate_limit_per_user",
        "default_auto_archive_duration", "type", "bitrate", "user_limit", "rtc_region", "video_quality_mode",
    )

    def __init__(self, data: MsgVoiceChannel) -> None:
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self.guild_id: int = int(data["guild_id"])
        self.position: int = data["position"]
        self.permission_overwrites: List[PermissionOverwrite] = data["permission_overwrites"]
        self.parent_id: Optional[Snowflake] = data.get("parent_id", None)
        self.topic: str = data["topic"]
        self.last_message_id: Optional[Snowflake] = data.get("last_message_id", None)
        self.last_pin_timestamp: Optional[str] = data.get("last_pin_timestamp", None)
        self.rate_limit_per_user: Optional[int] = data.get("rate_limit_per_user", None)
        self.default_auto_archive_duration: Optional[
            ThreadArchiveDuration
        ] = data.get("default_auto_archive_duration", None)
        self.type: Literal[2] = data["type"]
        self.bitrate: int = data.get("bitrate", 0)
        self.user_limit: Optional[int] = data.get("user_limit", 0)
        self.rtc_region: Optional[str] = data.get("rtc_region")
        self.video_quality_mode: Optional[VideoQualityMode] = data.get("video_quality_mode")

    def __repr__(self) -> str:
        return f"<VoiceChannel id={self.id} name={self.name!r}>"

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "guild_id": self.guild_id,
            "position": self.position,
            "topic": self.topic,
            "last_message_id": self.last_message_id,
            "rate_limit_per_user": self.rate_limit_per_user,
            "default_auto_archive_duration": self.default_auto_archive_duration,
            "type": self.type,
            "bitrate": self.bitrate,
            "user_limit": self.user_limit,
            "rtc_region": self.rtc_region,
            "video_quality_mode": self.video_quality_mode,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        return cls(data)
