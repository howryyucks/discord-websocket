"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

from typing import Any, Optional, Dict, Union, List

from disws.types import (
    Embed as MsgEmbed,
    FooterEmbed,
    ImageEmbed,
    ThumbnailEmbed,
    VideoEmbed,
    ProviderEmbed,
    EmbedAuthor,
    EmbedField,
)
from disws.utils import from_iso_format_to_humanly


class Embed:
    __slots__ = (
        "title",
        "type",
        "description",
        "url",
        "color",
        "timestamp",
        "footer",
        "image",
        "thumbnail",
        "video",
        "provider",
        "author",
        "fields",
    )

    def __init__(self, data: MsgEmbed) -> None:
        self.type: Optional[Union[str, int]] = data.get("type", None)
        self.color: Optional[int] = data.get("color", None)
        self.title: Optional[str] = data.get("title", None)
        self.description: Optional[str] = data.get("description", None)
        self.url: str = data.get("url")
        self.timestamp: Optional[str] = (
            from_iso_format_to_humanly(data["timestamp"])
            if data.get("timestamp", None)
            else None
        )
        self.footer: Optional[FooterEmbed] = data.get("footer", None)
        self.image: Optional[ImageEmbed] = data.get("image", None)
        self.thumbnail: Optional[ThumbnailEmbed] = data.get("thumbnail", None)
        self.video: Optional[VideoEmbed] = data.get("video", None)
        self.provider: Optional[ProviderEmbed] = data.get("provider", None)
        self.author: Optional[EmbedAuthor] = data.get("author", None)
        self.fields: Optional[List[EmbedField]] = data.get("fields", None)

    @property
    def created_at(self) -> Optional[str]:
        return self.timestamp or "None"

    def __repr__(self) -> str:
        return f"<Embed title={self.title!r}>"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "type": self.type,
            "description": self.description,
            "url": self.url,
            "timestamp": self.created_at,
            "color": self.color,
            "footer": self.footer,
            "image": self.image,
            "thumbnail": self.thumbnail,
            "video": self.video,
            "provider": self.provider,
            "author": self.author,
            "fields": self.fields,
        }
