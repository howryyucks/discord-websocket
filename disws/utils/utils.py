"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""
from datetime import datetime
from enum import StrEnum
from typing import Optional, Union, Callable, overload, Type, Generic, TypeVar, Any, Dict, List

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)

flags: Dict[int, str] = {
    1 << 0: "Staff Team",
    1 << 1: "Guild Partner",
    1 << 2: "HypeSquad Events Member",
    1 << 3: "Bug Hunter Level 1",
    1 << 5: "Dismissed Nitro promotion",
    1 << 6: "House Bravery Member",
    1 << 7: "House Brilliance Member",
    1 << 8: "House Balance Member",
    1 << 9: "Early Nitro Supporter",
    1 << 10: "Team Supporter",
    1 << 14: "Bug Hunter Level 2",
    1 << 16: "Verified Bot",
    1 << 17: "Early Verified Bot Developer",
    1 << 18: "Moderator Programs Alumni",
    1 << 19: "Bot uses only http interactions",
    1 << 22: "Active Developer"
}


class WebSocketStatus:
    reconnect = 7
    resume = 6
    init = 2


class CachedSlotProperty(Generic[T, T_co]):
    def __init__(self, name: str, function: Callable[[T], T_co]) -> None:
        self.name = name
        self.function = function
        self.__doc__ = getattr(function, '__doc__')

    @overload
    def __get__(self, instance: None, owner: Type[T]) -> "CachedSlotProperty[T, T_co]":
        ...

    @overload
    def __get__(self, instance: T, owner: Type[T]) -> T_co:
        ...

    def __get__(self, instance: Optional[T], owner: Type[T]) -> Any:
        if instance is None:
            return self

        try:
            return getattr(instance, self.name)
        except AttributeError:
            value = self.function(instance)
            setattr(instance, self.name, value)
            return value


def cached_slot_property(name: str) -> Callable[[Callable[[T], T_co]], CachedSlotProperty[T, T_co]]:
    def decorator(func: Callable[[T], T_co]) -> CachedSlotProperty[T, T_co]:
        return CachedSlotProperty(name, func)

    return decorator


def get_flag(public_flag: int) -> str:
    flags_all: List[str] = list()
    for key, value in flags.items():
        if (key and public_flag) == key:
            flags_all.append(value)
        flags_all.append(value)
    return ', '.join(flags_all)


def get_avatar_url(user_id: int, avatar: Optional[str]) -> Optional[str]:
    avatar = (
        f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}."
        f"{'gif' if str(avatar).startswith('a_') else 'png'}"
        if avatar
        else None
    )
    return avatar


def guild_member_avatar_url(guild_id: int, user_id: int, avatar: Optional[str]) -> Optional[str]:
    avatar = (
        f"https://cdn.discordapp.com/guilds/{guild_id}/users/{user_id}/avatars/{avatar}."
        f"{'gif' if str(user_id).startswith('a_') else 'png'}"
        if avatar
        else None
    )
    return avatar


def get_role_icon_url(role_id: int, role_icon: Optional[str]) -> Optional[str]:
    role_icon = (
        f"https://cdn.discordapp.com/role-icons/{role_id}/{role_icon}.png"
        if role_icon
        else None
    )
    return role_icon


def get_guild_icon_url(guild_id: int, server_icon: Optional[str]) -> Optional[str]:
    server_icon = (
        f"https://cdn.discordapp.com/icons/{guild_id}/{server_icon}."
        f"{'gif' if str(server_icon).startswith('a_') else 'png'}"
        if server_icon
        else None
    )
    return server_icon


def get_guild_banner_url(guild_id: int, banner: Optional[str]) -> Optional[str]:
    banner = (
        f"https://cdn.discordapp.com/banners/{guild_id}/{banner}."
        f"{'gif' if str(banner).startswith('a_') else 'png'}"
        if banner
        else None
    )
    return banner


def get_guild_splash_url(guild_id: int, splash: Optional[str]) -> Optional[str]:
    splash = (
        f"https://cdn.discordapp.com/splashes/{guild_id}/{splash}.png"
        if splash
        else None
    )
    return splash


def get_banner_url(user_id: int, banner: Optional[str]) -> Optional[str]:
    banner = (
        f"https://cdn.discordapp.com/banners/{user_id}/{banner}."
        f"{'gif' if str(banner).startswith('a_') else 'png'}"
        if banner
        else None
    )
    return banner


def get_member_create_date(
        user_id: Union[str, int],
        to_string: str = "%d.%m.%Y %H:%M:%S",
) -> Optional[str]:
    if user_id == -1:
        return None

    user_creation: float = ((int(user_id) >> 22) + 1420070400000) / 1000.0
    creation_date: str = datetime.fromtimestamp(user_creation).strftime(to_string)
    return creation_date


def has_nitro(premium_type: Optional[int]) -> str:
    return (
        "No nitro"
        if premium_type == 0
        else "Nitro Classic"
        if premium_type == 1
        else "Nitro Boost"
        if premium_type == 2
        else "Nitro Basic"
    )


def from_timestamp_to_humanly(
        timestamp: Union[float, int], to_string: str = "%d.%m.%Y %H:%M:%S"
) -> str:
    return datetime.fromtimestamp(timestamp / 1000.0).strftime(to_string)


def from_iso_format_to_humanly(
        iso: str, to_string: str = "%d.%m.%Y %H:%M:%S"
) -> Optional[str]:
    try:
        date = datetime.fromisoformat(iso)
    except (ValueError, TypeError):
        return iso
    return date.strftime(to_string)


class EventStatus(StrEnum):
    READY = "READY"
    PRESENCE_UPDATE = "PRESENCE_UPDATE"
    MESSAGE_CREATE = "MESSAGE_CREATE"
    CHANNEL_CREATE = "CHANNEL_CREATE"
    GUILD_MEMBER_UPDATE = "GUILD_MEMBER_UPDATE"
    GUILD_AUDIT_LOG_ENTRY_CREATE = "GUILD_AUDIT_LOG_ENTRY_CREATE"
    CHANNEL_UPDATE = "CHANNEL_UPDATE"
    MESSAGE_DELETE = "MESSAGE_DELETE"
    MESSAGE_UPDATE = "MESSAGE_UPDATE"
    SESSIONS_REPLACE = "SESSIONS_REPLACE"
    MESSAGE_REACTION_ADD = "MESSAGE_REACTION_ADD"
    MESSAGE_REACTION_REMOVE = "MESSAGE_REACTION_REMOVE"
    MESSAGE_ACK = "MESSAGE_ACK"
    VOICE_STATE_UPDATE = "VOICE_STATE_UPDATE"
    CALL_CREATE = "CALL_CREATE"
    CALL_UPDATE = "CALL_UPDATE"
    CALL_DELETE = "CALL_DELETE"
    TYPING_START = "TYPING_START"
