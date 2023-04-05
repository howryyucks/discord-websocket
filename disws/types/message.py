"""
discord-websocket (disws, ver 0.0.6)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

from datetime import datetime
from typing import List, NotRequired, Optional, TypedDict, Union

from . import Embed, Role
from .other import AllowedMentionType, MessageActivityType, Snowflake, SnowflakeList
from .user import User


class PartialMessage(TypedDict):
    channel_id: Snowflake
    guild_id: NotRequired[Snowflake]


class MessageActivity(TypedDict):
    type: MessageActivityType
    party_id: str


class MessageApplication(TypedDict):
    id: Snowflake
    description: str
    icon: Optional[str]
    name: str
    cover_image: NotRequired[str]


class MessageReference(TypedDict, total=False):
    message_id: Snowflake
    channel_id: Snowflake
    guild_id: Snowflake
    fail_if_not_exists: bool


class Attachment(TypedDict):
    id: Snowflake
    url: str
    proxy_url: str
    filename: str
    size: int
    height: NotRequired[int]
    width: NotRequired[int]
    description: NotRequired[str]
    content_type: NotRequired[str]
    spoiler: NotRequired[bool]
    ephemeral: NotRequired[bool]


class Message(PartialMessage):
    id: Snowflake
    author: Union[User, None]
    content: str
    timestamp: Union[datetime, str]
    edited_timestamp: Union[datetime, str, None]
    pinned: bool
    tts: bool
    mention_everyone: bool
    mentions: list[Union[User, None]]
    referenced_message: NotRequired[Optional["Message"]]
    mention_roles: Optional[List[Role]]
    member: User
    embeds: Optional[List[Embed]]
    components: Optional[List[None]]
    attachments: Optional[List[Attachment]]


class AllowedMentions(TypedDict):
    parse: List[AllowedMentionType]
    roles: SnowflakeList
    users: SnowflakeList
    replied_user: bool
