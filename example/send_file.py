import asyncio
import io
import logging

from disws import Client, File


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


client = MyClient(token="your_token", bot=True)  # or bot=False if you entered a user-token


async def main() -> None:
    channel = await client.get_channel(...)  # input channel id

    while not client.is_ready:  # wait until client is ready
        logging.info("Waiting for client to be ready...")
        await asyncio.sleep(2)

    await client.send_message(
        channel=channel,  # you can also input channel_id in string or integer
        silent=True,
        attachments=[
            File(fp=io.StringIO("Hello world!"), filename="example.txt"),  # send from io.StringIO()
            File(fp="example.txt", filename="example.txt"),  # or you can input name of file
        ]
    )
    await client.close()


client.run(func=main)  # without ()
