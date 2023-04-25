"""
discord-websocket (disws, ver 0.0.6)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""
from .channel import TextChannel, VoiceChannel, ChannelCache
from .guild import Guild, GuildCache
from .message import Message, MessageCache

__version__ = "0.0.6"
__author__ = "Howry Yucks"
__license__ = "GNU GPL 3"

message_cache = MessageCache()
guild_cache = GuildCache()
channel_cache = ChannelCache()

# PEP 8 moment, bruh
import logging

from .attachment import Attachment, File
from .base.websocket import Client
from .embed import Embed
from .emoji import Emoji
from .role import Role
from .user import Me, Member, User

# basic logging
logging.basicConfig(
    format="%(levelname)s: [%(asctime)s] %(module)s (line: %(lineno)d): %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
