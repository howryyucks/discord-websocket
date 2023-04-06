"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Self, Union

from disws.types import Message as Msg
from disws.utils import from_iso_format_to_humanly
from .attachment import Attachment
from .embed import Embed
from .guild import Guild
from .user import Member


class Message:
    __slots__ = (
        "id", "__guild_data", "timestamp", "pinned",
        "tts", "referenced_message", "guild", "mentions",
        "mention_roles", "mention_everyone", "embeds", "edited_timestamp",
        "content", "components", "attachments", "channel_id", "author", "guild_id",
    )

    def __init__(self, data: Msg, guild_data: Dict[str, Any] = None) -> None:
        self.id: int = int(data["id"])
        self.__guild_data = guild_data or {}
        self.timestamp: Union[
            datetime, str
        ] = from_iso_format_to_humanly(data["timestamp"]) if data.get("timestamp", None) else None
        self.pinned: bool = data.get("pinned", False)
        self.tts: bool = data.get("tts", False)
        self.referenced_message: Optional[Message] = data.get("referenced_message", None)
        self.mention_roles: Union[List, None] = data.get("mention_roles", None)
        self.mention_everyone: bool = data.get("mention_everyone", False)
        self.embeds: Optional[List[Embed]] = [
            Embed(embed) for embed in data["embeds"]
        ] if data.get("embeds", None) else None
        self.edited_timestamp: Union[datetime, str, None] = from_iso_format_to_humanly(
            data["edited_timestamp"]) if data.get("edited_timestamp", None) else None
        self.content: str = data.get("content", "")
        self.guild: Optional[Guild] = Guild(
            self.__guild_data["guild"]
        ) if self.__guild_data.get("guild", None) else None
        self.mentions = self.fill_mentions(data["mentions"]) if data.get("mentions", None) else []
        self.components: Union[List, None] = data.get("components", None)
        self.attachments: Union[List[Attachment], None] = [
            Attachment(data=attachment) for attachment in data["attachments"]
        ] if data.get("attachments", None) else None
        self.channel_id: Optional[int] = int(data["channel_id"]) if data.get("channel_id", None) else None
        self.author: Optional[Member] = Member(data["author"]) if data.get("author", None) else None
        self.guild_id: Optional[int] = int(data["guild_id"]) if data.get("guild_id", None) else None

    def __repr__(self):
        return f"<message={self.content!r}, id={self.id}>," \
               f" attachments={len(self.attachments) if self.attachments else 0}>"

    def fill_mentions(self, data: List[Dict[Any, Any]]) -> List[Member]:
        mentions_list = []
        for mention in data:
            if mention is None:
                break

            if isinstance(mention, dict):
                mentions_list.append(
                    Member(
                        mention,
                        guild=self.guild.to_dict()
                        if getattr(self, "guild", None)
                        else None
                    )
                )
        return mentions_list

    def to_dict(self) -> Dict[Any, Any]:
        embeds_dict = []
        mentions_dict = []
        attachments_dict = []

        if self.embeds:
            for embed in self.embeds:
                embeds_dict.append(embed.to_dict())

        if self.attachments:
            for attachment in self.attachments:
                attachments_dict.append(attachment.to_dict())

        if self.mentions:
            for mention in self.mentions:
                mention = mention.to_dict()
                mention["guild"] = self.guild.to_dict() if getattr(self, "guild", None) else None
                mentions_dict.append(mention)

        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "pinned": self.pinned,
            "tts": self.tts,
            "referenced_message": self.referenced_message,
            "mentions": mentions_dict,
            "mention_roles": self.mention_roles,
            "mention_everyone": self.mention_everyone,
            "embeds": embeds_dict,
            "edited_timestamp": self.edited_timestamp,
            "content": self.content if self.content is not None else "",
            "components": self.components,
            "attachments": attachments_dict,
            "channel_id": self.channel_id,
            "author": self.author.to_dict(),
            "guild_id": self.guild_id,
        }

    @property
    def created_at(self) -> Union[datetime, str]:
        return self.timestamp

    @property
    def edited_at(self) -> str:
        return self.edited_timestamp or "Not edited"

    @classmethod
    def from_dict(cls, data: Dict[Any, Any], guild_data: Dict[Any, Any] = None) -> Self:
        return cls(data=data, guild_data=guild_data)


class MessageCache:
    messages: Dict[int, Union[Dict[Any, Any], Message]] = {}

    def __init__(self) -> None:
        pass

    def add_message(
        self, message_id: Union[int, str], message: Union[Dict[Any, Any], "Message"]
    ) -> Union[Dict[Any, Any]]:
        if isinstance(message, dict):
            self.messages[message_id] = Message.from_dict(message)
        else:
            self.messages[message_id] = message
        return self.messages[message_id]

    def get_message(self, message_id: int) -> Union[Dict[Any, Any], Message, None]:
        return self.messages.get(message_id, None)

    def mark_message_as_deleted(
        self, message_id: int, convert_to_dict: bool = False
    ) -> Union[Dict[Any, Any], "Message"]:
        result: Union[Dict[Any, Any], "Message"] = self.messages.pop(message_id, None)
        if convert_to_dict:
            result = result.to_dict()
        return result

    def mark_message_as_edited(
        self, message_id: int, new_message: Union[Dict[Any, Any], Message], guild_data: Dict[Any, Any] = None
    ) -> tuple[Union[Dict[Any, Any], Message, str], Union[Dict[Any, Any], Message, str]]:
        if self.messages.get(message_id, None) is not None:
            old_message = self.messages[message_id]
            self.messages[message_id] = Message(new_message, guild_data=guild_data) \
                if isinstance(new_message, dict) else new_message
            self.messages[message_id].edited_timestamp = datetime.now().timestamp()
            return old_message, self.messages[message_id]
        else:
            return "Not cached", "Not cached"
