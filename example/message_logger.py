import logging
from typing import Union

from disws import Client, Message


class MyClient(Client):
    async def on_ready(self) -> None:
        """
        When client is ready
        """
        logging.info("Client is ready")

    async def on_connect(self) -> None:
        """
        When client is connected
        """
        logging.info("Client is connected to WebSocket")

    async def on_message_create(self, message: Message) -> None:
        """
        When message is created
        """
        logging.info(f"\nNew message:\nMessage -> {message}\nMessage dict: -> {message.to_dict()}")

    async def on_message_update(self, before: Message, after: Message) -> None:
        """
        When message is edited
        """
        logging.info(f"\nUpdated message:\nOld -> {before}"
                     f"\nOld message dict: -> {before.to_dict()}"
                     f"\nNew -> {after}\nNew message dict: -> {after.to_dict()}")

    async def on_message_delete(self, message: Union["Message", dict]) -> None:
        """
        When message is deleted
        """
        logging.info(f"\nDeleted message:\nMessage -> {message}\nMessage dict: -> {message.to_dict()}")


client = MyClient(token="your_token", bot=True)  # or bot=False if you entered a user-token
client.run()  # in this example, parameter func is not required
