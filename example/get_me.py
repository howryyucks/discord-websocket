import logging

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
        print(message)


client = MyClient(token="your_token", bot=True)  # or bot=False if you entered a user-token


async def main() -> None:
    me = await client.get_me()
    print(f"Info about {me.full_name}\nDict -> {me.to_dict()}")
    await client.close()


client.run(func=main)  # without ()
