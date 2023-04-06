"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

from typing import List, Literal, Optional, Type, TypedDict, Union

Snowflake: Type[Union[str, int]] = Union[str, int]
SnowflakeList: Type[List[Union[int, str]]] = List[Snowflake]
PremiumType: Type[int] = Literal[0, 1, 2, 3]
MessageActivityType: Type[int] = Literal[1, 2, 3, 5]
AllowedMentionType: Type[str] = Literal["roles", "users", "everyone"]


class PartialEmoji(TypedDict):
    id: Optional[Snowflake]
    name: Optional[str]


class Reaction(TypedDict):
    count: int
    me: bool
    emoji: PartialEmoji


class PermissionOverwrite(TypedDict):
    id: Snowflake
    type: Literal[0, 1]
    allow: bool
    deny: bool
