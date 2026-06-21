---
title: Celery Reference
---

# Celery Reference

Pinned: `celery[redis]==5.6.3`, `django-celery-beat==2.9.0`, `django-celery-results==2.6.0`. Requires Redis broker.

## Install

```bash
pip install "celery[redis]==5.6.3" "django-celery-beat==2.9.0" "django-celery-results==2.6.0"
python manage.py migrate django_celery_beat django_celery_results
```

## `core/celery.py`

Project-shared Celery app. Lives in the `core` package so every app can `from celery import shared_task`.

```python
# core/celery.py
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
```

## `core/__init__.py`

```python
from core.celery import app as celery_app

__all__ = ("celery_app",)
```

Forces Celery to initialize at Django startup so `@shared_task` binds to this app.

## `core/settings.py` (CELERY namespace)

```python
from core.utils.env import env

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default="redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = "django-db"

CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_RESULT_EXTENDED = True
CELERY_TASK_TRACK_STARTED = True
CELERY_RESULT_EXPIRES = 86400
DJANGO_CELERY_BEAT_TZ_AWARE = True
```

```python
INSTALLED_APPS = [
    # ...
    "django_celery_beat",
    "django_celery_results",
]
```

## App-level tasks

```python
# apps/myapp/tasks.py
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task(bind=True)
def slow_job(self, item_id):
    # ORM / side effects here
    return item_id
```

`autodiscover_tasks()` loads `tasks.py` from each installed app.

## Run commands

```bash
celery -A core worker -l info
celery -A core beat -l info

# dev shortcut: combined worker + beat
celery -A core worker --beat -l info
```

## Enqueue after DB commit (REQUIRED for write paths)

Tasks **must** run after the surrounding transaction commits — otherwise workers may pick up a row that does not yet exist.

```python
from django.db import transaction

# Manual: works on all Celery versions
@transaction.atomic
def create_user_view(request):
    user = User.objects.create(username=request.POST["username"])
    transaction.on_commit(lambda: send_welcome_email.delay(user.pk))
    return HttpResponse("ok")

# Shortcut: Celery >= 5.4
@transaction.atomic
def create_article(request):
    article = Article.objects.create()
    expand_abbreviations.delay_on_commit(article.pk)
    return HttpResponseRedirect("/articles/")
```

## Rules of thumb

- **Never** pass ORM instances as task args — pass PKs and refetch inside the task.
- **Never** use the `pickle` serializer — keep JSON.
- **Always** wrap write-then-enqueue in `transaction.atomic` + `on_commit` / `delay_on_commit`.
- Idempotent task bodies; assume the broker may redeliver.
- Set explicit `time_limit` / `soft_time_limit` on long-running tasks.
