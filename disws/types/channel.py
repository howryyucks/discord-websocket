"""
discord-websocket (disws, ver 0.0.6)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

from typing import Any, List, Literal, NotRequired, Optional, Type, TypedDict, Union

from .guild import Guild
from .other import PermissionOverwrite, Snowflake
from .thread import ThreadArchiveDuration, ThreadMember, ThreadMetadata, ThreadType
from .user import PartialUser

ChannelTypeWithoutThread: Type[int] = Literal[0, 1, 2, 3, 4, 5, 6, 13, 15]
ChannelType: Type[int] = Union[ChannelTypeWithoutThread, ThreadType]
VideoQualityMode: Type[int] = Literal[1, 2]
PrivacyLevel: Type[int] = Literal[2]


class _BaseChannel(TypedDict):
    id: Snowflake
    name: str


class _BaseGuildChannel(_BaseChannel):
    guild_id: Snowflake
    position: int
    permission_overwrites: List[PermissionOverwrite]
    nsfw: bool
    parent_id: Optional[Snowflake]


class _BaseTextChannel(_BaseGuildChannel, total=False):
    topic: str
    last_message_id: Optional[Snowflake]
    last_pin_timestamp: str
    rate_limit_per_user: int
    default_auto_archive_duration: ThreadArchiveDuration


class ChannelMention(TypedDict):
    id: Snowflake
    type: ChannelType
    guild_id: Snowflake


class TextChannel(_BaseTextChannel):
    type: Literal[0]
    guild: Guild


class NewsChannel(_BaseTextChannel):
    type: Literal[5]


class VoiceChannel(_BaseTextChannel):
    type: Literal[2]
    bitrate: int
    user_limit: int
    rtc_region: NotRequired[Optional[str]]
    video_quality_mode: NotRequired[VideoQualityMode]


class CategoryChannel(_BaseGuildChannel):
    type: Literal[4]


class StageChannel(_BaseGuildChannel):
    type: Literal[13]
    bitrate: int
    user_limit: int
    rtc_region: NotRequired[Optional[str]]
    topic: NotRequired[str]


class ThreadChannel(_BaseChannel):
    type: Literal[10, 11, 12]
    guild_id: Snowflake
    parent_id: Snowflake
    owner_id: NotRequired[Snowflake]
    nsfw: bool
    last_message_id: NotRequired[Optional[Snowflake]]
    rate_limit_per_user: NotRequired[int]
    message_count: int
    member_count: int
    thread_metadata: ThreadMetadata
    member: NotRequired[ThreadMember]

    last_pin_timestamp: NotRequired[str]
    flags: NotRequired[int]


class ForumChannel(_BaseGuildChannel):
    type: Literal[15]


GuildChannel: Type[Any] = Union[
    TextChannel, NewsChannel, VoiceChannel,
    CategoryChannel, StageChannel, ThreadChannel,
    ForumChannel]


class DMChannel(_BaseChannel):
    type: Literal[1]
    last_message_id: Optional[Snowflake]
    recipients: List[PartialUser]
    is_message_request: NotRequired[bool]
    is_message_request_timestamp: NotRequired[str]
    is_spam: NotRequired[bool]


class GroupDMChannel(_BaseChannel):
    type: Literal[3]
    icon: Optional[str]
    owner_id: Snowflake
    recipients: List[PartialUser]


Channel: Type[Any] = Union[GuildChannel, DMChannel, GroupDMChannel]


class StageInstance(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    channel_id: Snowflake
    topic: str
    privacy_level: PrivacyLevel
    discoverable_disabled: bool
    guild_scheduled_event_id: Optional[int]
