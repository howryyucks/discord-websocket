"""
discord-websocket (disws, ver 0.0.6)

2023-2023

source code: https://github.com/howryyucks/discord-websocket
"""

from typing import Any, Dict, Literal, Optional, Union

from aiohttp import ClientResponse, ClientSession, ClientTimeout, FormData


class BaseRequest:
    BASE_URL = "https://discord.com/"

    def __init__(self, session: Optional[ClientSession] = None) -> None:
        self.session = session

    async def send_request(
        self,
        url: str,
        method: Literal["GET", "DELETE", "POST", "PATCH", "PUT"] = "GET",
        json: Union[Dict[Any, Any], FormData] = None,
        json_data: Union[Dict[Any, Any], str] = None,
        params: Dict[Any, Any] = None,
        headers: Dict[Any, Any] = None,
    ) -> Optional[ClientResponse]:
        """
        Send a request to the Discord API.
        :param params: Parameters to the request.
        :param url: URL to send the request to.
        :param method: HTTP method to use.
        :param json: JSON data to send.
        :param headers: Headers to the request.
        :return: :class:`ClientResponse` object
        """
        t_url = None

        payload = {}
        if params is not None:
            t_url = url.replace(self.BASE_URL, "")

            data_json = ""

            if method in ["GET", "DELETE"]:
                if params:
                    strl = []
                    for name, value in params.items():
                        strl.append(f"{name}={value}")
                    data_json += "&".join(strl)
                    t_url += f"?{data_json}"
        if headers is None:
            headers = {}

        if not url.startswith(self.BASE_URL):
            url = f"{self.BASE_URL}{t_url if t_url else url}"

        if method == "GET":
            return await self.session.get(url, json=json, headers=headers)

        elif method == "POST":
            return await self.session.post(
                url, json=json_data or payload or json, headers=headers
            )

        elif method == "DELETE":
            return await self.session.delete(url, headers=headers, json=json)

        elif method == "PUT":
            return await self.session.put(
                url, data=json_data or payload, headers=headers
            )

        elif method == "PATCH":
            return await self.session.patch(
                url, data=payload, headers=headers, json=json
            )

        return None

    async def force_exit(self):
        """
        Force exit from the :class:`ClientSession` object.
        :return: None
        """
        return await self.session.close()

    async def __aenter__(self):
        if self.session is None or self.session.closed:
            self.session = ClientSession(timeout=ClientTimeout(10))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
