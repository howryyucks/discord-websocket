"""
discord-websocket (disws, ver 0.0.6)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

import asyncio.exceptions
import json
import logging
import os
import re
import time
import zlib
from traceback import format_exc
from typing import Union, Dict, Any, Optional

import websockets.exceptions

from disws.base.client import BaseClient
from disws.utils import Intents, WebSocketStatus, EventStatus
from .errors import DiscordTokenError
from ..channel import TextChannel, VoiceChannel
from ..message import Message
from ..user import Member


# aiohttp.http_websocket.


class Client(BaseClient):
    # OP Codes
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE = 3
    VOICE_STATE = 4
    VOICE_PING = 5
    RESUME = 6
    RECONNECT = 7
    REQUEST_MEMBERS = 8
    INVALIDATE_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11
    GUILD_SYNC = 12

    last_ping_time: float = 0

    def __init__(self, token: str, api_num: int = 10, bot: bool = False) -> None:
        """
        The Discord Web Socket Client.

        :param token: The Discord Web Socket token.

        :param api_num: (Optional) The Discord API version.

        :param bot: (Optional) Whether the client is a bot.

        :raises ValueError: If the token is not a valid Discord token, or is not provided.
        :returns: Client
        """
        self.__pattern_token = r"\b[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"
        if not token:
            raise DiscordTokenError(text="Token is required.")

        if re.search(self.__pattern_token, token) is None:
            raise DiscordTokenError(text=f"\"{token}\" is not a discord token.")

        super().__init__(f"Bot {token}" if bot else token)
        self.bot = bot

        self._api_url = f"wss://gateway.discord.gg/?v={api_num}&encoding=json&compress=zlib-stream"
        self.token = f"Bot {token}" if self.bot else token

        self.zlib = zlib.decompressobj()
        self.zlib_suffix = b'\x00\x00\xff\xff'

        self.ws = None

        self.work: bool = False
        self.ready: bool = False

        self.loop: Optional[asyncio.AbstractEventLoop] = None

    def _gen_payload(self, op_code: Union[int, str] = None) -> Dict[str, Any]:
        intents = Intents().get_intents() if self.bot else None

        return {
            "op": self.IDENTIFY if not op_code else op_code,
            "d": {
                "token": self.token,
                "intents": intents,
                "properties": {"$os": "linux", "$browser": "disws", "$device": "pc"},
                "compress": True,
            },
        }

    def run(self, func: Any = None) -> None:
        """
        Runs the Client.

        :param func: (optional) The coroutine function to run.
        :return: None
        """
        logging.info("Running Discord Client...")
        self.loop = asyncio.get_event_loop()

        if func:
            if not asyncio.iscoroutinefunction(func):
                raise ValueError(f"function \"{func.__name__}\" must be a coroutine.")
            self.loop.create_task(func())

        self.work = True
        try:
            self.loop.run_until_complete(self.connect())
        except KeyboardInterrupt:
            self.loop.create_task(self.close())
            os._exit(0)  # type: ignore

    async def _connect(self) -> None:
        try:
            await self.send_ws_message(self._gen_payload(WebSocketStatus.init))
        except KeyboardInterrupt:
            await self.close()
            exit(0)

    @staticmethod
    async def close() -> None:
        """
        Finally closes the Web Socket connection.
        :return: Nothing
        """
        logging.info("Closing...")
        os._exit(0)  # type: ignore

    @staticmethod
    async def reconnect() -> None:
        """
        Reconnects to the Web Socket.
        :return: None
        """
        logging.fatal("Please re-run this program")
        os._exit(0)  # type: ignore

    async def _send_ping(self):
        try:
            await self.send_ws_message({"op": 1, "d": time.time()})
            logging.debug("Successfully sent heartbeat")
        except (Exception, BaseException):
            logging.error(format_exc())

    async def heartbeat(self, interval: float) -> None:
        """
        Sends a heartbeat to the Web Socket.
        :param interval: The interval in seconds.
        :return: None
        """
        while self.work:
            try:
                await self._send_ping()
                await asyncio.sleep(interval)
                self.last_ping_time = time.perf_counter()
            except asyncio.CancelledError:
                break

    def heartbeat_interval(self) -> float:
        """
        Gets the heartbeat interval in seconds.
        :return: The heartbeat interval in seconds.
        """
        return self.last_ping_time - time.perf_counter()

    @property
    def ping(self) -> float:
        """
        Gets the ping interval in seconds.
        :return: The heartbeat interval in seconds.
        """
        return self.last_ping_time - time.perf_counter()

    @property
    def is_ready(self) -> bool:
        """
        Checks if the Web Socket connection is ready.
        :return: True if the connection is ready, False otherwise.
        """
        return self.ready

    async def receive_ws_message(self) -> None:
        """
        Receives the Web Socket message.
        :return: None
        """
        value = await self.ws.recv()
        b_array = bytearray()
        b_array.extend(value)

        if len(value) < 4 or value[-4:] != self.zlib_suffix:
            return

        if value:
            item = self.zlib.decompress(value)
            item = json.loads(item)

            op_code = item.get('op')  # Op code
            data = item.get('d')  # Data
            event = item.get('t')  # The event

            if op_code == self.RECONNECT:
                logging.info(f"OP Code: {op_code}. Reconnecting...")
                await self.reconnect()

            elif op_code == self.RESUME:
                self.loop.create_task(self.trigger("on_resume"))

            elif op_code == self.INVALIDATE_SESSION:
                logging.info(f"OP Code: {op_code} (Invalidate session). Closing...")
                if data:
                    await self.close()

            elif op_code == self.HELLO:
                interval = data['heartbeat_interval'] / 1000.0
                identify_dict = self._gen_payload()
                await self.send_ws_message(message=identify_dict)
                self.loop.create_task(self.heartbeat(interval))
                self.loop.create_task(self.trigger("on_connect"))

            elif op_code == self.HEARTBEAT_ACK:
                self.heartbeat_interval()

            elif op_code == self.DISPATCH:
                guild = None

                if event == EventStatus.READY:
                    self.loop.create_task(self.trigger("on_ready"))
                    self.ready = True

                if event == EventStatus.GUILD_MEMBER_UPDATE:
                    result = Member(data["user"])
                    await self.trigger("on_guild_member_update", result)

                if isinstance(data, dict) and data.get("guild_id", None):
                    member = data.get("member")
                    if member:
                        guild = {
                            "guild": (
                                    self.guild_cache.try_get(str(data["guild_id"]))
                                    or
                                    self.guild_cache.add_guild(str(data["guild_id"]), await self.get_guild(
                                        data["guild_id"],
                                        headers=self.headers,
                                        to_dict=True
                                    ))
                            ),
                            "nick": member.get("nick", None),
                            "avatar": member.get("avatar", None),
                            "roles": member.get("roles", []),
                            "joined_at": member.get("joined_at", None),
                            "premium_since": member.get("premium_since", None),
                            "deaf": member.get("deaf", False),
                            "mute": member.get("mute", False),
                            "flags": member.get("flags", 0),
                            "pending": member.get("pending", False),
                            "permissions": member.get("permissions", None),
                            "communication_disabled_until": member.get("communication_disabled_until", None),
                        }

                if event == EventStatus.CHANNEL_CREATE:
                    channel = (
                        TextChannel(data)
                        if data.get("type", None) == 0
                        else VoiceChannel(data)
                        if data.get("type", None) == 1
                        else None
                    )
                    self.channel_cache.add_channel(data.get("id"), channel)
                    self.loop.create_task(self.trigger("on_channel_create", channel))

                if event == EventStatus.CHANNEL_UPDATE:
                    before = self.channel_cache.try_get(data.get("id"))
                    after = (
                        TextChannel(data)
                        if data.get("type", None) == 0
                        else VoiceChannel(data)
                        if data.get("type", None) == 1
                        else None
                    )
                    print(before, after)
                    self.loop.create_task(self.trigger("on_channel_update", before, after))

                if event == EventStatus.MESSAGE_CREATE:
                    result = Message.from_dict(data, guild_data=guild)
                    self.message_cache.add_message(data["id"], result)
                    self.loop.create_task(self.trigger("on_message_create", result))

                if event == EventStatus.MESSAGE_DELETE:
                    result = self.message_cache.mark_message_as_deleted(data["id"], convert_to_dict=False)
                    self.loop.create_task(self.trigger("on_message_delete", result))

                if event == EventStatus.MESSAGE_UPDATE:
                    before, after = self.message_cache.mark_message_as_edited(data["id"], data, guild)
                    self.loop.create_task(self.trigger("on_message_edit", before, after))

    async def connect_to_ws(self):
        """
        Connects to the Web Socket.
        :return: None
        """
        if self.work:
            logging.info("Connecting to WebSocket...")
            try:
                self.ws = await websockets.connect(self._api_url, origin="https://discord.com")
                self.work = True
            except (Exception, BaseException) as e:
                raise Exception
        else:
            logging.info("Exiting...")
            os._exit(0)  # type: ignore

    async def connect(self) -> None:
        await self.connect_to_ws()
        while self.work:
            try:
                await self.receive_ws_message()
            except KeyboardInterrupt:
                logging.info("Closing connection (user exit)")
                await self.close()
            except websockets.exceptions.ConnectionClosedError:
                await self.reconnect()
            except (Exception, BaseException):
                logging.info(format_exc())
                logging.info("Reconnecting...")
                await self.reconnect()

    async def send_ws_message(self, message: dict) -> None:
        """
        Sends a message to a Web Socket.
        :param message: The message to send Type: :type:`dict`
        :return: None
        """
        await self.ws.send(json.dumps(message))
