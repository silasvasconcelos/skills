---
title: Django Channels Reference
---

# Django Channels Reference

Pinned: `channels[daphne]==4.3.2`, `channels-redis==4.3.0`. Channels 4.3.x supports Django 4.2–6.0.

## Install

```bash
pip install "channels[daphne]==4.3.2" "channels-redis==4.3.0"
```

`channels[daphne]` pulls Daphne ≥4.0 and overrides `runserver` with an ASGI version (HTTP + WebSocket).

## `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    "daphne",  # MUST be first
    "django.contrib.admin",
    # ...
    "channels",
    "apps.myapp",
]
```

## `core/asgi.py`

```python
# core/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django_asgi_app = get_asgi_application()

from apps.myapp.routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
```

Import `routing` **after** `get_asgi_application()` so the app registry is ready.

## `core/settings.py`

```python
from core.utils.env import env

ASGI_APPLICATION = "core.asgi.application"

REDIS_URL = env.str("REDIS_URL", default="redis://127.0.0.1:6379/0")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [REDIS_URL]},
    },
}
```

For `rediss://` with self-signed certs use a dict form with `"address"` + `"ssl_cert_reqs": None`.

## App consumer + routing

```python
# apps/myapp/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": data["message"]},
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
```

```python
# apps/myapp/routing.py
from django.urls import re_path

from apps.myapp import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
```

`group_send` `type` `chat.message` is dispatched to handler `chat_message` (dot → underscore).

## Run

```bash
# dev / prod ASGI (Channels recommended)
daphne -b 0.0.0.0 -p 8000 core.asgi:application

# alternative ASGI server
uvicorn core.asgi:application --host 0.0.0.0 --port 8000

# channel-layer background workers (if used)
python manage.py runworker
```

With `daphne` first in `INSTALLED_APPS`, `python manage.py runserver` becomes Daphne's ASGI dev server (HTTP + WebSocket). Without `channels[daphne]`, stock `runserver` stays WSGI-only.

## Rules of thumb

- **Always** wrap the websocket router in `AllowedHostsOriginValidator` to enforce host checks.
- **Never** call sync ORM directly from an async consumer — wrap with `channels.db.database_sync_to_async`.
- Use `group_send` / `group_add` for broadcast; do not store channel names in the DB long-term (they expire).
- One Redis (or compatible) instance handles both Channels and Celery in most setups — keep DSNs in `.env`.
