"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

from datetime import datetime
from typing import TypedDict, Union


class FooterEmbed(TypedDict):
    text: str
    icon_url: str
    proxy_url: str


class ImageEmbed(TypedDict):
    url: str
    proxy_url: str
    height: int
    width: int


class ThumbnailEmbed(TypedDict):
    url: str
    proxy_url: str
    height: int
    width: int


class VideoEmbed(TypedDict):
    url: str
    proxy_url: str
    height: int
    width: int


class ProviderEmbed(TypedDict):
    name: str
    url: str


class EmbedAuthor(TypedDict):
    name: str
    url: str
    icon_url: str
    proxy_url: str


class EmbedField(TypedDict):
    name: str
    value: str
    inline: bool


class Embed(TypedDict):
    title: str
    type: int
    description: str
    url: str
    timestamp: Union[datetime, str, None]
    color: int
    footer: FooterEmbed
    image: ImageEmbed
    thumbnail: ThumbnailEmbed
    video: VideoEmbed
    provider: ProviderEmbed
    author: EmbedAuthor
    fields: list[EmbedField]
