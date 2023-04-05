import asyncio

from disws import Client
from disws.utils import log


class MyClient(Client):
    async def on_event(self, event) -> None:
        """When receiver web socket event"""
        if not event or "op" not in event:
            return

        if event["op"] == 10:
            log.info("Connecting to discord WebSocket...")

        if event["op"] == 11:
            log.info("Connected to discord WebSocket.")


async def main() -> None:
    client = MyClient(token="your_token", bot=True)  # or bot=False if you entered a user-token
    client.run()

    guild = await client.get_guild(guild_id=..., to_dict=False)  # input guild id
    print(f"Info about {guild.name} guild\nDict -> {guild.to_dict()}")

    client.stop()

    while True:
        await asyncio.sleep(2)


asyncio.run(main())
