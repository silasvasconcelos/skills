# Django Middleware Reference (5.0+)

## How Middleware Works

Middleware processes requests/responses in order. Request flows top-down through `MIDDLEWARE`, response flows bottom-up.

```
Request  →  Middleware 1  →  Middleware 2  →  ... →  View
Response ←  Middleware 1  ←  Middleware 2  ←  ... ←  View
```

## Built-in Middleware

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",           # HTTPS redirects, HSTS
    "django.contrib.sessions.middleware.SessionMiddleware",    # Session support
    "django.middleware.common.CommonMiddleware",               # URL normalization, APPEND_SLASH
    "django.middleware.csrf.CsrfViewMiddleware",               # CSRF protection
    "django.contrib.auth.middleware.AuthenticationMiddleware", # request.user
    "django.contrib.messages.middleware.MessageMiddleware",    # Messages framework
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # X-Frame-Options
    "django.contrib.auth.middleware.LoginRequiredMiddleware",  # global login required [5.1+]
    "django.middleware.csp.ContentSecurityPolicyMiddleware",   # CSP [6.0+]
    "django.middleware.locale.LocaleMiddleware",               # i18n (after Session, before Common)
    "django.middleware.gzip.GZipMiddleware",                   # Gzip compression (before any body-altering)
]
```

## Custom Middleware

### Function-Based

```python
def simple_middleware(get_response):
    def middleware(request):
        # Pre-processing (before view)
        request.start_time = time.time()

        response = get_response(request)

        # Post-processing (after view)
        duration = time.time() - request.start_time
        response["X-Request-Duration"] = str(duration)
        return response

    return middleware
```

### Class-Based

```python
class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - request.start_time
        response["X-Request-Duration"] = str(duration)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Called before the view. Return None or HttpResponse."""
        return None

    def process_exception(self, request, exception):
        """Called if view raises an exception. Return None or HttpResponse."""
        return None

    def process_template_response(self, request, response):
        """Called if response has render() method. Must return a response."""
        return response
```

### Async Middleware

```python
class AsyncTimingMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response

    async def __call__(self, request):
        start = time.time()
        response = await self.get_response(request)
        response["X-Duration"] = str(time.time() - start)
        return response
```

### Hybrid Middleware (Sync + Async)

```python
import asyncio
from asgiref.sync import iscoroutinefunction

class HybridMiddleware:
    async_capable = True
    sync_capable = True

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    def __call__(self, request):
        if iscoroutinefunction(self):
            return self.__acall__(request)
        response = self.get_response(request)
        return response

    async def __acall__(self, request):
        response = await self.get_response(request)
        return response
```

## Middleware Hooks

| Hook | When Called | Return |
|------|-----------|--------|
| `__call__` | Every request | HttpResponse |
| `process_view` | Before view, after URL resolution | None or HttpResponse |
| `process_exception` | When view raises exception | None or HttpResponse |
| `process_template_response` | After view, if response has `render()` | Response with `render()` |

## LoginRequiredMiddleware [5.1+]

Requires authentication for all views by default. Views that should remain public must be explicitly exempted.

```python
# settings.py
MIDDLEWARE = [
    ...
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.LoginRequiredMiddleware",
    ...
]
LOGIN_URL = "/accounts/login/"
```

```python
# Exempt public views
from django.contrib.auth.decorators import login_not_required

@login_not_required
def public_homepage(request):
    ...

# For class-based views
from django.utils.decorators import method_decorator

@method_decorator(login_not_required, name="dispatch")
class PublicView(View):
    ...
```

## Common Patterns

### IP-Based Access Control

```python
class IPBlockMiddleware:
    BLOCKED_IPS = ["1.2.3.4"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        if ip in self.BLOCKED_IPS:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Blocked")
        return self.get_response(request)
```

### Request Logging

```python
import logging

logger = logging.getLogger("django.request")

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"{request.method} {request.path}")
        response = self.get_response(request)
        logger.info(f"{request.method} {request.path} -> {response.status_code}")
        return response
```

### Maintenance Mode

```python
from django.conf import settings
from django.http import HttpResponse

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, "MAINTENANCE_MODE", False):
            if not request.user.is_staff:
                return HttpResponse("Site under maintenance", status=503)
        return self.get_response(request)
```
