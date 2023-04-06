"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""
import json
from typing import Optional, List, Dict, Any, Union, overload

from aiohttp import FormData

from disws.base.errors import HTTPException
from disws.base.guild import DiscordGuild
from .api_base import BaseRequest
from .. import File
from ..channel import TextChannel
from ..embed import Embed
from ..message import Message


class DiscordChannel(BaseRequest):
    def __init__(self, headers: Dict[Any, Any] = None) -> None:
        super().__init__()
        self.headers = headers or {}
        self.guild = DiscordGuild()

    async def get_channel(self, channel_id: int) -> TextChannel:
        """
        Get a channel by id.
        :param channel_id: id of the channel
        :return: :class:`TextChannel` object
        """
        async with self:
            response = await self.send_request(
                f"/api/v10/channels/{channel_id}", method="GET", headers=self.headers
            )
            if response.status == 200:
                response = await response.json()
                guild = await self.guild.get_guild(response["guild_id"], headers=self.headers, to_dict=True)
                response["guild"] = guild
                return TextChannel(response)

            else:
                raise HTTPException(status_code=response.status, text=await response.json())

    @overload
    async def send_message(
        self,
        channel: Union[TextChannel, str, int],
        *,
        content: Optional[str] = None,
        silent: Optional[bool] = False,
        embeds: Optional[List[Embed]] = None,
        attachments: Optional[List[File]] = None
    ) -> Optional[Message]:
        """
        Send a message to a channel.
        :param channel: Channel ID to send the message (type: :class:`TextChannel`, :class:`str` or :class:`int`)
        :param content: Message content
        :param silent: Send message silently (default: False)
        :param embeds: List of :class:`disws.Embed` objects
        :param attachments: List of :class:`disws.File` object

        :raise HTTPException: If the request fails for any reason program calls :class:`disws.base.errors.HTTPException`
        :raise ValueError: if the request has too many attachments (max 10)
        :return: Created :class:`Message` object
        """
        ...

    @overload
    async def send_message(
        self,
        channel: Union[TextChannel, str, int],
        *,
        content: Optional[str] = None,
        silent: Optional[bool] = False,
        embeds: Optional[List[Embed]] = None,
        attachments: Optional[File] = None
    ) -> Optional[Message]:
        """
        Send a message to a channel.
        :param channel: Channel ID to send the message (type: :class:`TextChannel`, :class:`str` or :class:`int`)
        :param content: Message content
        :param silent: Send message silently (default: False)
        :param embeds: List of :class:`disws.Embed` objects
        :param attachments: Attachment in :class:`disws.File` object

        :raise HTTPException: If the request fails for any reason program calls :class:`disws.base.errors.HTTPException`
        :raise ValueError: if the request has too many attachments (max 10)
        :return: Created :class:`Message` object
        """
        ...

    async def send_message(
        self, channel: Union[TextChannel, str, int],
        *,
        content: Optional[str] = None,
        silent: Optional[bool] = False,
        **kwargs,
    ) -> Optional[Message]:
        """
        Send a message to a channel.
        :param channel: Channel ID to send the message (type: :class:`TextChannel`, :class:`str` or :class:`int`)
        :param content: Message content
        :param silent: Send message silently (default: False)

        :raise HTTPException: If the request fails for any reason program calls :class:`disws.base.errors.HTTPException`
        :raise ValueError: if the request has too many attachments (max 10)
        :return: Created :class:`Message` object
        """

        embed = kwargs.get("embeds", None)
        attachments = kwargs.get('attachments', None)

        if embed:
            embeds = [
                embed.to_dict()
                if getattr(embed, "to_dict", None)
                else embed
                for embed in kwargs['embeds']
                if isinstance(embed, Embed)
            ]
        else:
            embeds = []

        channel_id = channel.id if isinstance(channel, TextChannel) else channel
        data = FormData()
        payload = {
            'flags': 4096 if silent else 0,
            'content': content if content else '',
            'embeds': embeds,
        }
        data.add_field('payload_json', json.dumps(payload))

        if payload.get('embeds', None) is not None:
            data.add_field('embeds', json.dumps(payload['embeds']))

        if attachments:
            if not isinstance(attachments, list):
                data.add_field(f'files[0]', attachments.fp,  # type: ignore
                               filename=attachments.filename,  # type: ignore
                               content_type='application/octet-stream')
            else:
                if len(attachments) >= 11:
                    raise ValueError("Too many attachments (max 10)")

                for n, attachment in enumerate(attachments):
                    data.add_field(f'files[{n}]', attachment.fp,
                                   filename=attachment.filename,
                                   content_type='application/octet-stream')

        async with self:
            response = await self.send_request(
                f"/api/v10/channels/{channel_id}/messages",
                method="POST",
                json=data,
                headers=self.headers
            )
            if response.status == 200:
                return Message(await response.json())
            else:
                raise HTTPException(status_code=response.status, text=await response.json())
