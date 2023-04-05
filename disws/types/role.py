"""
discord-websocket (disws, ver 0.0.6)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""
from typing import TypedDict

from disws.types.other import Snowflake


class RoleTags(TypedDict):
    bot_id: Snowflake
    integration_id: Snowflake
    premium_subscriber: None
    subscription_listing_id: Snowflake
    available_for_purchase: None
    guild_connections: None


class Role(TypedDict):
    id: Snowflake
    name: str
    color: int
    hoist: bool
    icon: str
    unicode_emoji: str
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: RoleTags
