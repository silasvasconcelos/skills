---
title: django-environ Reference
---

# django-environ Reference

Pinned: `django-environ==0.13.0`. No `INSTALLED_APPS` entry; import-only.

## Install

```bash
pip install django-environ==0.13.0
```

## `core/utils/env.py`

The single place that instantiates `environ.Env` and reads `.env`. Every `settings.py` import goes through this module so defaults and types live in one place.

```python
# core/utils/env.py
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, ""),
    DJANGO_ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
    DATABASE_CONN_MAX_AGE=(int, 600),
)

environ.Env.read_env(BASE_DIR / ".env")
```

## `core/settings.py` usage

```python
from core.utils.env import BASE_DIR, env

SECRET_KEY = env.str("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

DATABASES = {"default": env.db_url("DATABASE_URL")}
DATABASES["default"]["CONN_MAX_AGE"] = env.int("DATABASE_CONN_MAX_AGE")

CACHES = {
    "default": env.cache_url("CACHE_URL", default="locmemcache://"),
    "redis": env.cache_url("REDIS_URL", default="rediscache://127.0.0.1:6379/1"),
}

EMAIL_CONFIG = env.email_url("EMAIL_URL", default="consolemail://")
vars().update(EMAIL_CONFIG)

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default="redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", default=CELERY_BROKER_URL)

if not DEBUG:
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

## `.env.example` template

Commit this file. **Never** commit the real `.env`.

```dotenv
# Django core
DJANGO_SECRET_KEY=change-me-local-only
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (postgres | postgresql | psql | sqlite:///path)
DATABASE_URL=postgres://user:password@127.0.0.1:5432/mydb

# Cache (locmem | rediscache | redis://...)
CACHE_URL=locmemcache://
REDIS_URL=rediscache://127.0.0.1:6379/1

# Celery
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

# Email (smtp | smtp+tls | consolemail | filemail | ...)
EMAIL_URL=consolemail://

# Allauth social providers
GOOGLE_OAUTH_CLIENT_ID=
GOOGLE_OAUTH_SECRET=

# JWT (optional override)
# DJANGO_JWT_SIGNING_KEY=
```

URL-encode unsafe credential characters (`#`, `@`, …) with `urllib.parse.quote`.

## Cast cheat sheet

| Method | Returns |
|--------|---------|
| `env.str(var, default=...)` | String |
| `env.bool(var)` | `true`/`on`/`yes`/`1` → `True` |
| `env.int(var)` / `env.float(var)` | Numeric |
| `env.list(var)` | Comma-separated → `list[str]` |
| `env.db_url(var)` | DB DSN → `DATABASES` dict |
| `env.cache_url(var)` | Cache DSN → `CACHES` dict |
| `env.email_url(var)` | Email DSN → `EMAIL_*` dict |

`env.db()` / `env.cache()` / `env.email()` shortcuts read the canonical `DATABASE_URL` / `CACHE_URL` / `EMAIL_URL` names.

Membership check: `if "SENTRY_DSN" in env: ...`

## Security rules

- **Never** commit `.env`. Add it to `.gitignore`. Commit only `.env.example` with placeholder values.
- **Production**: inject real values from the platform's secret store / env (12-factor). Avoid on-disk `.env` files in prod.
- For Docker/K8s file-mounted secrets use `environ.FileAwareEnv()` so `SECRET_KEY_FILE=/run/secrets/...` is read transparently.
- Do **not** set a default for `DJANGO_SECRET_KEY` in production code paths — missing var must raise `ImproperlyConfigured`.
- Set `env.warn_on_default = True` locally to surface `DefaultValueWarning` when defaults silently kick in.
