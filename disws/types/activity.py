from typing import TypedDict, Optional, Union


class ActivityTimestamp(TypedDict):
    start: Optional[int]
    end: Optional[int]


class ActivityEmoji(TypedDict):
    name: Optional[str]


class BaseActivity(TypedDict):
    type: int
    state: str
    name: str
    id: Union[str, int]
    emoji: ActivityEmoji
    # url: Optional[str]
    created_at: Optional[int]
    # application_id: Optional[str]
    # details: Optional[str]


class SpotifyParty(TypedDict):
    id: Optional[str]


class ActivityAsset(TypedDict):
    large_text: Optional[str]
    large_image: Optional[str]
    small_text: Optional[str]
    small_image: Optional[str]


class SpotifyActivity(BaseActivity):
    timestamps: ActivityTimestamp
    sync_id: Optional[str]
    session_id: Optional[str]
    party: Optional[SpotifyParty]
    flags: int
    details: Optional[str]
    assets: Optional[ActivityAsset]
    active: bool
