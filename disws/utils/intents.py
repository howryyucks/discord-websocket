"""
discord-websocket (disws, ver 0.0.6)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

from typing import List


class Intents:
    """
    Represents the Discord intents for bots of a :class:`disws.base.websocket.Client`.
    """

    intents = [
        'GUILDS', 'GUILD_MEMBERS', 'GUILD_BANS',
        'GUILD_EMOJIS_AND_STICKERS', 'GUILD_INTEGRATIONS', 'GUILD_WEBHOOKS',
        'GUILD_INVITES', 'GUILD_VOICE_STATES', 'GUILD_PRESENCES',
        'GUILD_MESSAGES', 'GUILD_MESSAGE_REACTIONS', 'GUILD_MESSAGE_TYPING',
        'DIRECT_MESSAGES', 'DIRECT_MESSAGE_REACTIONS', 'GUILD_SCHEDULED_EVENTS',
        'GUILD_SCHEDULED_EVENTS'
    ]

    @classmethod
    def get_intents_list(cls) -> List[str]:
        return cls.intents

    def get_intent(self, intent_name: str = "") -> int:
        for num, role in enumerate(self.intents):
            if role == intent_name:
                return 1 << num
        raise ValueError(f'Intent {intent_name} not found!')

    def get_intents(self, intents_list: List[str] = None) -> int:
        if not intents_list:
            intents_list = self.intents

        return sum([self.get_intent(intent) for intent in intents_list])
