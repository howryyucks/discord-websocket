import logging

from disws import Client


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


client = MyClient(
    token="your_token", bot=True
)  # or bot=False if you entered a user-token


async def main() -> None:
    channel = await client.get_channel(channel_id=...)  # input channel_id
    print(f"Info about {channel.name} channel\nDict -> {channel.to_dict()}")

    await client.close()


client.run(func=main)  # without ()
