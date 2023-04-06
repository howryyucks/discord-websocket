"""
discord-websocket (disws, ver 0.0.7)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""
import io
import os
from base64 import b64encode
from hashlib import md5
from typing import Any, Dict, Optional, Union, Tuple

from aiohttp import ClientSession

from disws.base.errors import HTTPException
from disws.types import Attachment as MsgAttachment
from .utils import cached_slot_property


class Attachment:
    __slots__ = (
        "id", "filename", "url", "content_type", "height", "width", "proxy_url",
        "description", "ephemeral", "size",
    )

    def __init__(self, *, data: MsgAttachment) -> None:
        self.id: int = int(data["id"])
        self.filename = data["filename"]
        self.url = data["url"]
        self.content_type: Optional[str] = data.get("content_type", None)
        self.height: Optional[int] = data.get("height", None)
        self.width: Optional[int] = data.get("width", None)
        self.proxy_url: Optional[str] = data.get("proxy_url", None)
        self.description: Optional[str] = data.get("description", None)
        self.ephemeral: bool = data.get("ephemeral", False)
        self.size: int = data.get("size", 0)

    def is_spoiler(self) -> bool:
        return self.filename.startswith("SPOILER_")

    def __repr__(self) -> str:
        return f"<Attachment id={self.id}, name={self.filename!r}, url={self.url!r}>"

    def __str__(self) -> str:
        return self.url or ""

    async def read_file(self, from_cache: bool = False) -> bytes:
        url: str = self.proxy_url or self.url if from_cache else self.url
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.read()
                else:
                    raise HTTPException(status_code=response.status, text="Attachment not found")

    async def save(
        self, file_path: Union[io.BufferedIOBase, str],
        seek: bool = True,
        from_cache: bool = False
    ) -> int:
        """
        Save the attachment into a file/PathLike/BufferedIOBase.

        :param file_path: The file/PathLike/BufferedIOBase to save the attachment
        :param seek: Whether to seek the file to the beginning
        :param from_cache: Whether to save from proxy_url
        :return: The file size
        """
        data = await self.read_file(from_cache=from_cache)
        if isinstance(file_path, io.BufferedIOBase):
            written = file_path.write(data)
            if seek:
                file_path.seek(0)
            return written
        else:
            file = file_path.split(self.filename)[0]
            os.makedirs(file, exist_ok=True)
            with open(file_path, "wb") as f:
                return f.write(data)

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "filename": self.filename,
            "id": self.id,
            "proxy_url": self.proxy_url,
            "size": self.size,
            "url": self.url,
            "spoiler": self.is_spoiler(),
        }
        if self.content_type:
            result["content_type"] = self.content_type
        if self.height:
            result["height"] = self.height
        if self.width:
            result["width"] = self.width
        if self.description:
            result["description"] = self.description
        if self.ephemeral:
            result["ephemeral"] = self.ephemeral
        return result


class File:
    """
    Taken from discord.py-self

    Link: https://github.com/dolfies/discord.py-self
    """
    __slots__ = ('fp', '_filename', 'spoiler', 'description', '_original_pos', '_owner', '_closer', '_cs_md5')

    def __init__(
        self,
        fp: Union[str, bytes, os.PathLike[Any], io.BufferedIOBase, io.StringIO],
        filename: Optional[str] = None,
        *,
        spoiler: bool = False,
        description: Optional[str] = None,
    ):
        """
        Helper class for uploading attachments into Discord.

        :param fp: The file/PathLike/BufferedIOBase/StringIO to upload
        :param filename: Send file with this filename
        :param spoiler: Mark file as spoiler
        :param description: Send file with this description

        :raises ValueError: If the file is not seekable and readable
        """
        if isinstance(fp, io.IOBase):
            if not (fp.seekable() and fp.readable()):
                raise ValueError(f"File buffer {fp!r} must be seekable and readable")
            self.fp: io.IOBase = fp
            self._original_pos: int = fp.tell()
            self._owner: bool = False
        else:
            self.fp: io = open(fp, 'rb')
            self._original_pos: int = 0
            self._owner: bool = True

        self._closer = self.fp.close
        self.fp.close = lambda: None

        if filename is None:
            if isinstance(fp, str):
                _, filename = os.path.split(fp)
            else:
                filename = getattr(fp, 'name', 'untitled')

        self._filename, filename_spoiler = self._strip_spoiler(filename)
        if spoiler is False:
            spoiler: bool = filename_spoiler

        self.spoiler: bool = spoiler
        self.description: Optional[str] = description

    @staticmethod
    def _strip_spoiler(filename: str) -> Tuple[str, bool]:
        stripped = filename
        if stripped.startswith('SPOILER_'):
            stripped = stripped[8:]
        spoiler = stripped != filename
        return stripped, spoiler

    @property
    def filename(self) -> str:
        return 'SPOILER_' + self._filename if self.spoiler else self._filename

    @filename.setter
    def filename(self, value: str) -> None:
        self._filename, self.spoiler = self._strip_spoiler(value)

    @cached_slot_property('_cs_md5')
    def md5(self) -> str:
        try:
            return b64encode(md5(self.fp.read()).digest()).decode('utf-8')
        finally:
            self.reset()

    def reset(self, *, seek: Union[int, bool] = True) -> None:
        if seek:
            self.fp.seek(self._original_pos)

    def close(self) -> None:
        self.fp.close = self._closer
        if self._owner:
            self._closer()

    def to_dict(self, index: int) -> Dict[str, Any]:
        payload = {
            'id': index,
            'filename': self.filename,
        }

        if self.description is not None:
            payload['description'] = self.description

        return payload
