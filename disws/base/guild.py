"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""
from typing import Dict, Any, Union

from disws import guild_cache
from disws.base.api_base import BaseRequest
from disws.base.errors import HTTPException
from ..guild import Guild
from ..user import Member


class DiscordGuild(BaseRequest):
    def __init__(self, headers: Dict[Any, Any] = None) -> None:
        super().__init__()
        self.headers = headers or {}

    async def get_guild(
            self, guild_id: int, headers: dict[any, any] = None,
            to_dict: bool = False, from_cache: bool = True
    ) -> Guild:
        """
        Get a guild by id.
        :param guild_id: Guild ID to find.
        :param headers: Headers to send with request.
        :param to_dict: If True, returns :class:`Guild` as a dictionary.
        :param from_cache: Returns :class:`Guild` from a :class:`GuildCache` object. Defaults to True.
        :return: :class:`Guild` object
        """
        global resp_json

        if from_cache:
            resp_json = guild_cache.try_get(guild_id=guild_id)

        if resp_json is None:
            async with self:
                response = await self.send_request(
                    f"/api/v10/guilds/{guild_id}", method="GET", headers=headers or self.headers
                )
                if response.status == 200:
                    resp_json = await response.json()
                    owner_json = await self.get_guild_user(
                        guild_id=guild_id, user_id=resp_json["owner_id"], without_guild=True
                    )
                    resp_json["owner_data"] = owner_json.to_dict()
                    guild_cache.add_guild(guild_id=guild_id, guild=resp_json)
                else:
                    raise HTTPException(status_code=response.status, text=await response.json())
        return resp_json if to_dict else Guild(resp_json)

    async def get_guild_user(
            self, guild_id: int, user_id: int,
            headers: dict = None, without_guild: bool = False, to_dict: bool = False
    ) -> Union[Member, Dict[Any, Any]]:
        """
        Get a user by guild id.
        :param guild_id: Guild ID to find user.
        :param user_id: User ID to find.
        :param headers: Headers to send with request.
        :param without_guild: The guild parameter in :class:`Member` will be None
        :param to_dict: If True, returns :class:`Member` as a dictionary.
        :return: :class:`Member` object
        """
        async with self:
            response = await self.send_request(
                f"/api/v10/guilds/{guild_id}/members/{user_id}",
                method="GET", headers=headers or self.headers
            )
            if response.status == 200:
                json_r = await response.json()
                member = json_r["user"]
                guild = {
                    "guild": (await self.get_guild(guild_id)).to_dict(),
                    "nick": json_r.get("nick", None),
                    "avatar": json_r.get("avatar", None),
                    "roles": json_r.get("roles", []),
                    "joined_at": json_r.get("joined_at", None),
                    "premium_since": json_r.get("premium_since", None),
                    "deaf": json_r.get("deaf", False),
                    "mute": json_r.get("mute", False),
                    "flags": json_r.get("flags", 0),
                    "pending": json_r.get("pending", False),
                    "permissions": json_r.get("permissions", None),
                    "communication_disabled_until": json_r.get("communication_disabled_until", None),
                } if not without_guild else None

                if to_dict:
                    member["guild"] = guild
                    return member
                return Member(member, guild)
            else:
                raise HTTPException(status_code=response.status, text=await response.json())
