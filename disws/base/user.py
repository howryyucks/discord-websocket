"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""
from typing import Dict, Any

from disws.base.api_base import BaseRequest
from disws.base.errors import HTTPException
from ..user import Me, Member


class DiscordUser(BaseRequest):
    def __init__(self, headers: Dict[Any, Any] = None) -> None:
        super().__init__()
        self.headers = headers or {}

    async def get_me(self) -> Me:
        """
        Get about Client User (Me).
        :return: :class:`Me` object
        """
        async with self:
            response = await self.send_request(
                "/api/v10/users/@me", method="GET", headers=self.headers
            )
            if response.status == 200:
                r_json = await response.json()
                return Me(r_json)
            else:
                raise HTTPException(
                    status_code=response.status, text=await response.json()
                )

    async def get_user(self, user_id: int) -> Member:
        """
        Get a user by id.
        :param user_id: ID to find.
        :return: :class:`Member` object
        """
        async with self:
            response = await self.send_request(
                f"/api/v10/users/{user_id}", method="GET", headers=self.headers
            )
            if response.status == 200:
                return Member(await response.json())
            else:
                raise HTTPException(
                    status_code=response.status, text=await response.json()
                )
