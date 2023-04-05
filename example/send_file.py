import asyncio
import io

from disws import Client, File
from disws.utils import log


class MyClient(Client):
    async def on_event(self, event) -> None:
        """Receive web socket event"""
        if not event or "op" not in event:
            return

        if event["op"] == 10:
            log.info("Connecting to discord WebSocket...")

        if event["op"] == 11:
            log.info("Connected to discord WebSocket.")


async def main() -> None:
    client = MyClient(token="your_token", bot=True)  # or bot=False if you entered a user-token

    client.run()

    channel = await client.get_channel(...)  # input channel id
    await client.send_message(
        channel=channel,  # you can also input channel_id in string or integer
        silent=True,
        attachments=[
            File(fp=io.StringIO("Hello world!"), filename="example.txt"),  # send from io.StringIO()
            File(fp="example.txt", filename="example.txt"),  # or you can input name of file
        ]
    )

    client.stop()

    while True:
        await asyncio.sleep(2)


asyncio.run(main())
