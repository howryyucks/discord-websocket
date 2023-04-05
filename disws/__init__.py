"""
discord-websocket (disws, ver 0.0.6)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

__version__ = "0.0.6"
__author__ = "Howry Yucks"
__license__ = "GNU GPL 3"

from .attachment import Attachment, File
from .base.websocket import Client
from .channel import TextChannel, VoiceChannel
from .embed import Embed
from .emoji import Emoji
from .guild import Guild
from .message import Message, MessageCache
from .role import Role
from .user import Me, Member, User
