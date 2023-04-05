import asyncio
from typing import Union

from disws import Client, Message
from disws.utils import log


class MyClient(Client):
    async def on_event(self, event) -> None:
        """When receive web socket event"""
        if not event or "op" not in event:
            return

        if event["op"] == 10:
            log.info("Connecting to discord WebSocket...")

        if event["op"] == 11:
            log.info("Connected to discord WebSocket.")

    async def on_message_create(self, message: Message) -> None:
        """
        When message is created
        """
        print(f"New message\nMessage -> {message}\nMessage dict: -> {message.to_dict()}")

    async def on_message_update(self, before: Message, after: Message) -> None:
        """
        When message is edited
        """
        print(f"Updated message\nOld -> {before}"
              f"\nOld message dict: -> {before.to_dict()}"
              f"\nNew -> {after}\nNew message dict: -> {after.to_dict()}")

    async def on_message_delete(self, message: Union["Message", dict]) -> None:
        """
        When message is deleted
        """
        print(f"Deleted message\nMessage -> {message}\nMessage dict: -> {message.to_dict()}")


async def main() -> None:
    client = MyClient(token="your_token", bot=True)  # or bot=False if you entered a user-token
    client.run()

    while True:
        await asyncio.sleep(5)


asyncio.run(main())
