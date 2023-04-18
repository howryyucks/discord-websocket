"""
discord-websocket (disws, ver 0.0.6)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""
import asyncio
from typing import Callable, Union, Tuple, Dict, Any

from aiohttp import ClientSession

from disws.base.api_base import BaseRequest
from disws.base.channel import DiscordChannel
from disws.base.guild import DiscordGuild
from disws.base.user import DiscordUser
from ..channel import TextChannel, VoiceChannel
from ..message import Message
from ..user import Member


class BaseClient(DiscordUser, DiscordChannel, DiscordGuild, BaseRequest):
    TIMEOUT = 10
    headers = {
        "content-type": "application/json",
        "user-agent": "Discord-WebSocket",
    }

    def __init__(self, token: str, api_version: int = None) -> None:
        super().__init__()
        self._token = token
        if api_version is not None:
            self.BASE_URL = f"https://discord.com/api/v{api_version}"

        self.session = ClientSession()
        self.headers["Authorization"] = self._token

        self._callbacks = {
            "on_event": [self.on_event],
            "on_guild_member_update": [self.on_guild_member_update],
            "on_message_create": [self.on_message_create],
            "on_message_delete": [self.on_message_delete],
            "on_message_edit": [self.on_message_update],
            "on_connect": [self.on_connect],
            "on_ready": [self.on_ready],
            "on_resume": [self.on_resume],
            "on_channel_create": [self.on_channel_create],
            "on_channel_update": [self.on_channel_update],
        }

    async def on(self, event_name: str, callback: Callable) -> None:
        """
        Create a custom callback function for an event.
        :param event_name: Event name to listen.
        :param callback: Callback function.
        :return: Adds the callback to the event.
        """
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError(
                f"Callback must be a coroutine function, not {type(callback)}"
            )
        if event_name not in self._callbacks:
            self._callbacks[event_name] = []
        self._callbacks[event_name].append(callback)

    async def trigger(self, event_name: str, before=None, after=None):
        """
        Trigger a callback function for an event
        :param event_name: Event name to listen.
        :param before: Before argument for the callback function.
        :param after: After argument for the callback function.
        :return: Callback function
        """
        if event_name in self._callbacks:
            for callback in self._callbacks[event_name]:
                # MSav moment
                try:
                    await callback(before, after)
                except TypeError:
                    try:
                        await callback(before)
                    except TypeError:
                        try:
                            await callback(after)
                        except TypeError:
                            try:
                                await callback()
                            except TypeError:
                                pass
            return

    @staticmethod
    async def on_event(event) -> None:
        pass

    @staticmethod
    async def on_connect() -> None:
        """
        Called when the client is connected to Discord Web Socket
        :return: None
        """
        return

    @staticmethod
    async def on_ready() -> None:
        """
        Called when the client is ready to receive events
        :return: None
        """
        return

    @staticmethod
    async def on_resume() -> None:
        """
        Called when the client is resumed from discord API
        :return: None
        """
        return

    @staticmethod
    async def on_guild_member_update(event: Member) -> "Member":
        """
        Called when a guild member is updated
        :param event: response from Discord API when a guild member is updated
        :return: :class:`Member` object
        """
        return event

    @staticmethod
    async def on_channel_create(channel: Union[TextChannel, VoiceChannel]) -> Union[TextChannel, VoiceChannel]:
        """
        Called when a channel is created
        :param channel: :class:`TextChannel` or :class:`VoiceChannel` object
        :return: :class:`TextChannel` or :class:`VoiceChannel` object
        """
        return channel

    @staticmethod
    async def on_channel_update(
            before: Union[TextChannel, VoiceChannel] = None,
            after: Union[TextChannel, VoiceChannel] = None,
    ) -> Tuple[Union[TextChannel, VoiceChannel], Union[TextChannel, VoiceChannel]]:
        """
        Called when a channel is updated
        :param before: :class:`TextChannel` or :class:`VoiceChannel` object before update
        :param after: :class:`TextChannel` or :class:`VoiceChannel` object after update
        :return: :class:`TextChannel` or :class:`VoiceChannel` objects
        """
        return before, after

    @staticmethod
    async def on_message_create(message: Message) -> "Message":
        """
        Called when a message is created
        :param message: :class:`Message` object from response
        :return: :class:`Message` object
        """
        return message

    @staticmethod
    async def on_message_update(before: Message, after: Message) -> Tuple["Message", "Message"]:
        """
        Called when a message is updated
        :param before: :class:`Message` object before update
        :param after: :class:`Message` object after update
        :return: :class:`Message`, :class:`Message` objects
        """
        return before, after

    @staticmethod
    async def on_message_delete(message: Union["Message", Dict[str, Any]]) -> Union["Message", Dict[str, Any]]:
        """
        Called when a message is deleted
        :param message: :class:`Message` object from :class:`MessageCache`
        :return: :class:`Message` object
        """
        return message
