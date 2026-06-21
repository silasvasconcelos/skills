# Django Async Reference (5.0+)

## Async Views

### Function-Based

```python
import asyncio
from django.http import HttpResponse, JsonResponse

async def async_view(request):
    data = await fetch_external_api()
    return JsonResponse(data)

async def concurrent_view(request):
    results = await asyncio.gather(
        fetch_api_a(),
        fetch_api_b(),
        fetch_api_c(),
    )
    return JsonResponse({"results": results})
```

### Class-Based

```python
from django.views import View

class AsyncArticleView(View):
    async def get(self, request, pk):
        article = await Article.objects.aget(pk=pk)
        return JsonResponse({"title": article.title})

    async def post(self, request, pk):
        ...
```

## Async ORM Queries

All QuerySet methods that execute SQL have `a`-prefixed async variants.

```python
# Async queryset methods
article = await Article.objects.aget(pk=1)
articles = await Article.objects.afilter(status="published")
exists = await Article.objects.filter(title="Test").aexists()
count = await Article.objects.acount()
first = await Article.objects.afirst()
last = await Article.objects.alast()

# Async create/update/delete
article = await Article.objects.acreate(title="New", content="Content")
await Article.objects.filter(pk=1).aupdate(status="published")
await Article.objects.filter(pk=1).adelete()
obj, created = await Article.objects.aget_or_create(title="Test", defaults={"content": "..."})
obj, created = await Article.objects.aupdate_or_create(title="Test", defaults={"content": "..."})

# Async iteration
async for article in Article.objects.filter(status="published"):
    print(article.title)

# Async aggregation
result = await Article.objects.aaggregate(avg_rating=Avg("rating"))

# Async model save/delete
article = Article(title="New", content="Content")
await article.asave()
await article.adelete()

# Async related objects
async for tag in article.tags.aall():
    print(tag.name)

book = await author.books.afirst()
await article.tags.aset([tag1, tag2])
await article.tags.aadd(tag3)
await article.tags.aremove(tag1)
await article.tags.aclear()
```

## sync_to_async and async_to_sync

```python
from asgiref.sync import sync_to_async, async_to_sync

# Wrap sync function for use in async context
@sync_to_async
def get_user_data(user_id):
    user = User.objects.get(pk=user_id)
    return {"name": user.name, "email": user.email}

async def my_async_view(request):
    data = await get_user_data(request.user.id)
    return JsonResponse(data)

# Wrap async function for use in sync context
@async_to_sync
async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com/data") as resp:
            return await resp.json()

# thread_sensitive parameter
sync_to_async(my_function, thread_sensitive=True)   # same thread (default, safe for DB)
sync_to_async(my_function, thread_sensitive=False)   # new thread (for CPU-bound work)
```

## Async Middleware

```python
class AsyncMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response

    async def __call__(self, request):
        # Pre-processing
        response = await self.get_response(request)
        # Post-processing
        return response
```

For best performance with ASGI, ensure all middleware is async-capable. Sync middleware between the ASGI handler and an async view causes extra thread context switches (~1ms each).

## ASGI Configuration

```python
# core/asgi.py
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
application = get_asgi_application()
```

```bash
# Run with uvicorn
uvicorn core.asgi:application --host 0.0.0.0 --port 8000

# Run with daphne
daphne core.asgi:application

# Run with hypercorn
hypercorn core.asgi:application
```

## Async Decorators (Compatible)

All these decorators work with both sync and async views:

- `cache_control()`, `never_cache()`
- `csrf_exempt()`, `csrf_protect()`, `ensure_csrf_cookie()`
- `require_http_methods()`, `require_GET()`, `require_POST()`, `require_safe()`
- `gzip_page()`
- `condition()`, `etag()`, `last_modified()`
- `vary_on_cookie()`, `vary_on_headers()`
- `login_required()`, `permission_required()`
- `csp_override()`, `csp_report_only_override()`

## Handling Disconnects

```python
import asyncio

async def long_running_view(request):
    try:
        result = await long_computation()
        return JsonResponse(result)
    except asyncio.CancelledError:
        # Client disconnected, clean up
        raise
```

## Limitations

1. **Transactions**: Not supported in async mode. Wrap transactional code in sync functions:
   ```python
   @sync_to_async
   def create_with_transaction():
       with transaction.atomic():
           obj = MyModel.objects.create(...)
           related = RelatedModel.objects.create(parent=obj)
       return obj
   ```

2. **Connection pooling**: Set `CONN_MAX_AGE = 0` in async mode, or use connection pooling:
   ```python
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.postgresql",
           "OPTIONS": {"pool": True},  # built-in pooling [5.1+]
       }
   }
   ```

3. **SynchronousOnlyOperation**: Parts of Django raise this in async contexts. Use `sync_to_async()` to wrap them. Never set `DJANGO_ALLOW_ASYNC_UNSAFE` in production.
