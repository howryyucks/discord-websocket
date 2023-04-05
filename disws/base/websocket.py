"""
discord-websocket (disws, ver 0.0.6)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

import asyncio.exceptions
import json
import os
import re
import time
from traceback import format_exc
from typing import Union

import websockets.exceptions

from disws.base.client import BaseClient
from disws.message import Message
from disws.utils import Intents, WebSocketStatus, log
from ..user import Member
from .errors import DiscordTokenError


class Client(BaseClient):
    last_ping_time: int = 0
    heartbeat_interval = 41250 / 1000
    sequence: Union[int, None] = None

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
        self._api_url = f"wss://gateway.discord.gg/?v={api_num}&encoding=json"
        self.token = f"Bot {token}" if self.bot else token
        self._conn = None
        self.ws: websockets.WebSocketClientProtocol = None
        self.wait = True

    def _get_ping_timeout(self) -> float:
        return self.heartbeat_interval

    def _gen_payload(self, op_code):
        intents = Intents().get_intents() if self.bot else None

        return {
            "op": op_code,
            "d": {
                "token": self.token,
                "intents": intents,
                "properties": {"$os": "linux", "$browser": "disws", "$device": "pc"},
                "compress": True,
            },
        }

    def run(self) -> None:
        """
        Runs the Client.
        :return: None
        """
        log.info("Running Discord Client...")
        self._conn = asyncio.ensure_future(self.connect())

    def stop(self) -> None:
        """
        Stops the Client.
        :return: None
        """
        log.info("Stopping Discord Client...")
        self._conn.cancel("Closing..")

    async def _connect(self) -> None:
        log.info("Connecting to WebSocket...")
        try:
            await self.send_ws_message(self._gen_payload(WebSocketStatus.init))
        except KeyboardInterrupt:
            await self._close()
            exit(0)

    async def _close(self) -> None:
        """
        Finally closes the Web Socket connection.
        :return: Nothing
        """
        log.info("Closing...")
        await self.ws.close()

    async def _reconnect(self, wait: bool = True) -> None:
        """
        Reconnects to the Web Socket.
        :param wait: (Optional) Whether to wait for reconnection.
        :return: None
        """
        log.info("Reconnecting...")
        await self._close()
        self.wait = wait
        self.run()

    async def _send_ping(self):
        start = int(time.time())
        await self.send_ws_message({"op": 1, "d": self.sequence})
        self.last_ping_time = int(time.time())
        log.info(f"WS ping: {self.last_ping_time - start}")

    async def connect(self) -> None:
        try:
            print("try...")
            async with websockets.connect(self._api_url) as session:
                self.ws = session
                await self._connect()
                log.warning("Connected")

                try:
                    while self.wait:
                        if (
                                not self.last_ping_time
                                or int(time.time()) - self.last_ping_time
                                > self._get_ping_timeout()
                        ):
                            await self._send_ping()
                        try:
                            evt = await asyncio.wait_for(
                                self.ws.recv(), timeout=self._get_ping_timeout()
                            )
                        except asyncio.TimeoutError:
                            await self._send_ping()
                        except asyncio.CancelledError:
                            await self.ws.ping()
                        except websockets.exceptions.ConnectionClosedError:
                            log.fatal(f"Error: {format_exc()}\nClosing...")
                            exit()
                        else:
                            try:
                                evt_obj = json.loads(evt)
                                if (
                                        evt_obj["op"] != 11
                                        and "s" in evt_obj
                                        and evt_obj["s"]
                                ):
                                    self.sequence = evt_obj["s"]
                                    if evt_obj["op"] == 10:
                                        self.heartbeat_interval = (
                                                int(evt_obj["d"]["heartbeat_interval"])
                                                / 1000
                                        )
                            except ValueError:
                                pass
                            else:
                                if evt_obj["op"] == 10:
                                    await self.trigger("on_connect")
                                if evt_obj["op"] == 11:
                                    await self.trigger("on_ready")

                                if evt_obj["t"] == "GUILD_MEMBER_UPDATE":
                                    result = Member(evt_obj["d"]["user"])
                                    await self.trigger("on_guild_member_update", result)
                                guild = None
                                if isinstance(evt_obj["d"], dict) and evt_obj["d"].get("guild_id", None):
                                    member = evt_obj["d"].get("member")
                                    if member:
                                        guild = {
                                            "guild": (
                                                await self.get_guild(evt_obj["d"]["guild_id"], headers=self.headers,
                                                                     to_dict=True)),
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
                                            "communication_disabled_until": member.get(
                                                "communication_disabled_until",
                                                None),
                                        }
                                if evt_obj["t"] == "MESSAGE_CREATE":
                                    result = Message.from_dict(evt_obj["d"], guild_data=guild)
                                    self.message_cache.add_message(
                                        evt_obj["d"]["id"], result
                                    )
                                    await self.trigger("on_message_create", result)
                                if evt_obj["t"] == "MESSAGE_DELETE":
                                    result = self.message_cache.mark_message_as_deleted(
                                        evt_obj["d"]["id"], convert_to_dict=False
                                    )
                                    await self.trigger("on_message_delete", result)
                                if evt_obj["t"] == "MESSAGE_UPDATE":
                                    # print(guild)
                                    before, after = self.message_cache.mark_message_as_edited(
                                        evt_obj["d"]["id"], evt_obj["d"], guild
                                    )
                                    await self.trigger("on_message_edit", before, after)

                except websockets.ConnectionClosed as e:
                    log.fatal(f"Error: {e} {format_exc()}")
                    await self._reconnect(wait=True)
                except asyncio.exceptions.CancelledError:
                    log.fatal(f"Error {format_exc()}\nExiting...")
                    os._exit(0)  # type: ignore
                except (BaseException, Exception) as e:
                    log.fatal(f"Error: {e} {format_exc()}")
                    await self._reconnect(wait=True)
        except GeneratorExit:
            log.fatal(f"Error {format_exc()}\nExiting...")
        except asyncio.exceptions.CancelledError:
            # log.fatal(f"Error {format_exc()}\nExiting...")
            os._exit(0)  # type: ignore
        except (Exception, BaseException) as e:
            log.fatal(f"Error: {e} {format_exc()}")
            await asyncio.sleep(2)
            await self._reconnect(wait=True)

    async def send_ws_message(self, message: dict) -> None:
        """
        Sends a message to a Web Socket.
        :param message: The message to send Type: :type:`dict`
        :return: None
        """
        await self.ws.send(json.dumps(message))
