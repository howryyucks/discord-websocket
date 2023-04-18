"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""
from typing import List, Literal, NotRequired, Optional, TypedDict, Dict, Any

from disws.types.emoji import Emoji
from disws.types.role import Role
from disws.types.user import PartialUser
from .other import Snowflake


class BaseGuild(TypedDict):
    id: Snowflake
    unavailable: bool


class WelcomeChannel(TypedDict):
    channel_id: Snowflake
    description: str
    emoji_id: NotRequired[Snowflake]
    emoji_name: NotRequired[str]


class GuildWelcomeScreen(TypedDict):
    description: str
    welcome_channels: List[WelcomeChannel]


class Sticker(TypedDict):
    id: Snowflake
    pack_id: Snowflake
    name: str
    description: str
    tags: str
    type: Literal[1, 2]
    format_type: Literal[1, 2, 3, 4]
    available: bool
    guild_id: Snowflake
    user: NotRequired[PartialUser]


class Guild(BaseGuild):
    name: str
    icon: str
    icon_hash: str
    splash: Optional[str]
    discovery_splash: Optional[str]
    user_is_owner: bool
    owner_id: Snowflake
    owner_data: Dict[Any, Any]
    permissions: str
    afk_channel_id: Optional[Snowflake]
    afk_timeout: int
    widget_enabled: bool
    widget_channel_id: Optional[Snowflake]
    verification_level: int
    default_message_notifications: int
    explicit_content_filter: int
    roles: List[Role]
    emojis: List[Emoji]
    mfa_level: int
    application_id: NotRequired[Optional[Snowflake]]
    system_channel_id: NotRequired[Optional[Snowflake]]
    system_channel_flags: NotRequired[int]
    rules_channel_id: NotRequired[Optional[Snowflake]]
    max_presences: int
    max_members: int
    vanity_url_code: Optional[str]
    description: str
    banner: NotRequired[Optional[str]]
    premium_tier: int
    premium_subscription_count: int
    preferred_locale: str
    public_updates_channel_id: NotRequired[Optional[Snowflake]]
    max_video_channel_users: int
    approximate_member_count: int
    approximate_presence_count: int
    welcome_screen: GuildWelcomeScreen
    nsfw_level: Literal[0, 1, 2, 3]
    stickers: NotRequired[List[Sticker]]
    premium_progress_bar_enabled: bool
