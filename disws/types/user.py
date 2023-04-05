"""
discord-websocket (disws, ver 0.0.6)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

from typing import NotRequired, Optional, TypedDict

from .other import PremiumType, Snowflake


class UserTag:
    __slots__ = ()
    id: int


class PartialUser(TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    avatar: Optional[str]
    avatar_decoration: NotRequired[Optional[str]]
    public_flags: NotRequired[int]
    bot: NotRequired[bool]
    system: NotRequired[bool]


class User(PartialUser, total=False):
    mfa_enabled: bool
    locale: str
    verified: bool
    email: Optional[str]
    flags: int
    purchased_flags: int
    premium_usage_flags: int
    premium_type: PremiumType
    banner: Optional[str]
    accent_color: Optional[int]
    bio: str
    analytics_token: str
    phone: Optional[str]
    token: str
    nsfw_allowed: Optional[bool]
