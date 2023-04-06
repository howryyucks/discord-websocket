"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""
from typing import List, NotRequired, TypedDict, Union, Optional

from disws.types.other import Snowflake
from disws.types.user import PartialUser, User
from .role import Role


class Emoji(TypedDict):
    id: Snowflake
    name: str
    roles: Optional[List[Role]]
    user: NotRequired[Union[User, PartialUser]]
    require_colons: bool
    managed: bool
    animated: bool
    available: bool
