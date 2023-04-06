## discord-websocket (known as disws)

**Developer release: 0.0.7**

Simple module for discord self-bots and bots (WebSocket + discord API)

### Features

- Asynchronous support
- Hybrid Support (support for bots and self-bots)

#### Requirements

- websocket
- aiohttp
- multidict

#### Installation:

To install release from pypi run:

```commandline
pip install disws
```

To install from development branch run:

```commandline
git clone https://github.com/howryyucks/discord-websocket.git
cd discord-websocket
python -m pip install -e .
```

#### Known issues:

- Emoji object: roles not converted (cause by error)
- **FIXED** ~~on_message_update/on_message_delete doesn't work with guild objects that use `mentions[index].guild`~~

#### TODO:

- [ ] Stickers class
- [ ] Thread class
- [x] Channel class (incomplete)

### Examples:
You can find examples in [examples directory](/example)
