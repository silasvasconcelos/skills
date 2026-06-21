---
name: django-superpowers
description: >-
  Comprehensive Django 5.0+ development skill covering models, views, forms,
  URLs, templates, admin, migrations, authentication, security, testing, async
  support, version-specific features (GeneratedField 5.0, LoginRequiredMiddleware
  5.1, Composite Primary Keys 5.2, Tasks framework 6.0), AND the recommended
  package stack: Django REST Framework, SimpleJWT, django-allauth (incl. headless
  + MFA), django-environ, Celery (with beat/results), and Django Channels. Use when
  bootstrapping a new Django project, installing/configuring DRF/allauth/JWT/Celery/Channels/environ,
  building Django applications, creating models, writing views, configuring URLs,
  handling forms, setting up authentication, writing tests, or working with any
  Django feature.
---

# Django Development Skill (5.0+)

## Version Support

This skill covers **Django 5.0 and above**. Features introduced in specific versions are annotated with version badges.

| Django Version | Python Requirement | Status |
|---|---|---|
| 5.0 | 3.10, 3.11, 3.12 | Security fixes only |
| 5.1 | 3.10, 3.11, 3.12, 3.13 | Security fixes only |
| 5.2 LTS | 3.10, 3.11, 3.12, 3.13, 3.14 | Supported (LTS) |
| 6.0 | 3.12, 3.13, 3.14 | Pre-release |

When a feature is annotated with a version (e.g., **[5.2+]**), it is only available in that version and later.

## Overview

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. This skill provides guidance for building Django applications following best practices and the official documentation.

## Core Principles

Every piece of code generated MUST follow these four principles. They are non-negotiable.

### 1. Performance-First Queries

- **Always** use `select_related()` for ForeignKey/OneToOneField access in querysets.
- **Always** use `prefetch_related()` for ManyToMany/reverse FK access.
- **Never** access related objects inside loops without prefetching (N+1 problem).
- Use `only()` / `defer()` to load only necessary fields in heavy queries.
- Use `values()` / `values_list()` when full model instances aren't needed.
- Use `exists()` instead of `count() > 0` or `len(qs) > 0`.
- Use `bulk_create()`, `bulk_update()` instead of looping `.save()`.
- Use `update()` / `delete()` on querysets for batch operations.
- Use `F()` expressions for database-level operations (avoid race conditions).
- Use `iterator()` for large querysets that don't need caching.
- Add database indexes (`db_index=True`, `Meta.indexes`) on frequently filtered/ordered fields.
- Use `Subquery` and `OuterRef` instead of Python-level filtering on related data.
- Use `assertNumQueries()` in tests to catch query regressions.

### 2. Security Always

- **Never** use `raw()`, `extra()`, or `RawSQL` with string interpolation. Always parameterize.
- **Never** use `|safe`, `mark_safe()`, or `{% autoescape off %}` on user input without sanitization.
- **Never** use `csrf_exempt` unless absolutely required (webhooks). Document why.
- **Always** validate and sanitize all input data (forms, serializers, query params).
- **Always** use `fields = [...]` explicitly on ModelForm/Serializer (never `__all__` in production).
- **Always** check object-level permissions (ownership) before mutation operations.
- Use `get_object_or_404()` to avoid information leakage via different error responses.
- Use `LoginRequiredMixin` / `@login_required` on every view that requires auth.
- Use `UserPassesTestMixin` / `PermissionRequiredMixin` for authorization checks.
- Use `select_for_update()` for critical write operations to prevent race conditions.
- Use `transaction.atomic()` for operations that must be all-or-nothing.
- Configure HTTPS, HSTS, secure cookies, CSP in production settings.
- Run `manage.py check --deploy` before every deployment.

### 3. DRY (Don't Repeat Yourself)

- **Always** organize models, querysets, and managers as packages — one class per module, re-exported from `__init__.py`.
- **Always** create a Custom QuerySet and Custom Manager for every model.
- **Always** create abstract base models for shared fields (timestamps, soft-delete, etc.).
- **Always** extract business logic into a Service Layer (`services.py`) to keep views thin.
- Use custom QuerySet methods chained together instead of repeating filter logic in views.
- Use model `@property` and methods for computed/derived data.
- Use mixins for shared view behavior (e.g., `OwnerRequiredMixin`).
- Use base serializers/forms for shared validation patterns.
- Use `transaction.atomic()` in service methods, not in views.
- Centralize permission checks in mixins or service layer, not scattered across views.
- Use `{% include %}` and template inheritance to avoid template duplication.

### 4. Django Best Practices

- **Never** generate migration files from AI. Migrations MUST only be created via `python manage.py makemigrations`. The AI may instruct the user to run the command but MUST NOT write or edit migration files directly.
- **Always** define `__str__()` on every model.
- **Always** define `get_absolute_url()` on models with detail views.
- **Always** set `related_name` on ForeignKey/M2M for explicit reverse access.
- **Always** use `reverse()` / `{% url %}` instead of hardcoded URLs.
- Keep views thin: views orchestrate, services execute, models encapsulate.
- Use `TextChoices` / `IntegerChoices` for all choice fields.
- Use `constraints` and `indexes` in `Meta` instead of deprecated `unique_together` / `index_together`.
- Use `update_fields` in `.save()` when only specific fields changed.
- Use `transaction.on_commit()` for side effects (emails, tasks) after successful transactions.
- Organize apps with clear boundaries: each app owns its `models/`, `querysets/`, `managers/`, services, and API.
- Write tests for models, views, forms, and services. Use `setUpTestData` for performance.

## Project Structure

The project uses a single `core` package for **both** project configuration **and** shared cross-app modules (models, serializers, views, utilities, Celery app). All business apps live under `apps/`. Models, QuerySets, and Managers within an app MUST be organized as packages (not single files).

```
project_root/
├── manage.py
├── .env                       # local secrets (NEVER commit)
├── .env.example               # committed template
├── pyproject.toml             # or requirements.txt
├── core/                      # Project config + shared modules
│   ├── __init__.py            # imports celery_app
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py                # Channels-aware ASGI app
│   ├── wsgi.py
│   ├── celery.py              # Celery app instance
│   ├── models.py              # Shared abstract models (TimeStampedModel, ...)
│   ├── serializers.py         # Shared DRF serializer bases / mixins
│   ├── views.py               # Shared DRF view bases / mixins
│   └── utils/
│       ├── __init__.py
│       └── env.py             # django-environ `env` singleton
├── apps/
│   ├── __init__.py
│   └── myapp/
│       ├── querysets/
│       │   ├── __init__.py           # re-exports all QuerySets
│       │   └── article_query_set.py  # ArticleQuerySet class
│       ├── managers/
│       │   ├── __init__.py           # re-exports all Managers
│       │   └── article_manager.py    # ArticleManager class
│       ├── models/
│       │   ├── __init__.py           # re-exports all models
│       │   └── article.py            # Article model
│       ├── migrations/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── views.py
│       ├── urls.py
│       ├── forms.py
│       ├── tasks.py           # Celery @shared_task / Django Tasks [6.0+]
│       ├── consumers.py       # Channels WebSocket consumers (optional)
│       ├── routing.py         # Channels websocket_urlpatterns (optional)
│       ├── serializers.py
│       ├── tests.py
│       └── templates/
│           └── myapp/
├── static/                    # Static assets (collected from STATICFILES_DIRS)
├── media/                     # User uploads (MEDIA_ROOT)
└── templates/                 # Project-wide templates
```

## Recommended Packages

A new Django project bootstrapped by this skill installs the following packages by default. Each has a dedicated reference file with pinned versions and configuration.

| Package | Purpose | Reference |
|---|---|---|
| `djangorestframework` | REST API framework | [drf-reference.md](references/drf-reference.md) |
| `djangorestframework-simplejwt` | JWT auth for DRF | [drf-reference.md](references/drf-reference.md) |
| `django-allauth[socialaccount,headless,mfa]` | Auth: email/social/MFA, headless API | [allauth-reference.md](references/allauth-reference.md) |
| `django-environ` | 12-factor settings via `.env` | [environ-reference.md](references/environ-reference.md) |
| `celery[redis]` + `django-celery-beat` + `django-celery-results` | Background tasks + scheduled jobs | [celery-reference.md](references/celery-reference.md) |
| `channels[daphne]` + `channels-redis` | WebSockets / ASGI | [channels-reference.md](references/channels-reference.md) |

Install everything in one go (omit extras you don't need):

```bash
pip install \
  "django~=5.2" \
  "djangorestframework~=3.17" \
  "djangorestframework-simplejwt~=5.5" \
  "django-allauth[socialaccount,headless,mfa]==65.17.0" \
  "django-environ==0.13.0" \
  "celery[redis]==5.6.3" "django-celery-beat==2.9.0" "django-celery-results==2.6.0" \
  "channels[daphne]==4.3.2" "channels-redis==4.3.0"
```

## Shared `core/` Modules

The `core` package owns both project configuration AND project-wide reusable code. Apps in `apps/` import from `core` for shared abstractions; **never** the reverse (no `core` → `apps` imports — that creates circular dependencies).

| Module | Contents |
|---|---|
| `core/settings.py` | Project settings; reads every secret through `core.utils.env.env` |
| `core/urls.py` | Root URLConf; includes app `urls.py`, JWT endpoints, allauth URLs |
| `core/asgi.py` | ASGI entrypoint; `ProtocolTypeRouter` for Channels |
| `core/wsgi.py` | WSGI entrypoint |
| `core/celery.py` | `Celery("core")` app; `autodiscover_tasks()` |
| `core/models.py` | Shared abstract models (`TimeStampedModel`, `SoftDeleteModel`, …) |
| `core/serializers.py` | Shared DRF serializer bases/mixins |
| `core/views.py` | Shared DRF view bases/mixins (e.g. `OwnedModelViewSet`) |
| `core/utils/env.py` | `env = environ.Env(...)` singleton — the **only** module that reads `.env` |

Example `core/models.py`:

```python
# core/models.py
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

App-level models inherit from these:

```python
# apps/myapp/models/article.py
from core.models import TimeStampedModel
```

## Bootstrapping a New Project

**All Django boilerplate MUST be generated by framework commands** — never hand-write `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`, `apps.py`, or app skeleton files. Edit them after generation.

```bash
# 1. Generate the project package named "core" at the repo root.
django-admin startproject core .

# 2. Create the apps namespace.
mkdir -p apps && touch apps/__init__.py

# 3. Scaffold an app inside apps/ (target directory MUST exist first).
mkdir -p apps/myapp
django-admin startapp myapp apps/myapp/

# 4. Create top-level asset directories.
mkdir -p static media templates
```

After `startapp`, edit `apps/myapp/apps.py` to use the dotted path:

```python
# apps/myapp/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MyappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.myapp"
    verbose_name = _("My App")
```

And set the default app config in `apps/myapp/__init__.py`:

```python
# apps/myapp/__init__.py
default_app_config = "apps.myapp.apps.MyappConfig"
```

Register the app in `core/settings.py` as `"apps.myapp"` (not `"myapp"`).

## Quick Command Reference

```bash
# Project setup (NEVER hand-write — always use these commands)
django-admin startproject core .
mkdir -p apps/myapp && django-admin startapp myapp apps/myapp/

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py sqlmigrate myapp 0001
python manage.py showmigrations

# Development
python manage.py runserver
python manage.py shell
python manage.py createsuperuser
python manage.py collectstatic

# Testing
python manage.py test
python manage.py test myapp
python manage.py test myapp.tests.TestClass.test_method

# Checks
python manage.py check
python manage.py check --deploy
python manage.py diffsettings
```

## Core Concepts

### Models

Define data models as Python classes inheriting from `models.Model`. **Always** use abstract base models for shared fields, Custom QuerySets for reusable query logic, and Custom Managers to expose them. Models, QuerySets, and Managers MUST be organized as packages (one class per module). Each model, QuerySet, and Manager MUST live in its own module inside the respective package.

**`myapp/querysets/article_query_set.py`**

```python
from django.db import models


class ArticleQuerySet(models.QuerySet):
    def published(self):
        from myapp.models import Article

        return self.filter(status=Article.Status.PUBLISHED)

    def by_author(self, user):
        return self.filter(author=user)

    def with_relations(self):
        return self.select_related("author").prefetch_related("tags")
```

**`myapp/querysets/__init__.py`**

```python
from myapp.querysets.article_query_set import ArticleQuerySet

__all__ = ["ArticleQuerySet"]
```

**`myapp/managers/article_manager.py`**

```python
from django.db import models

from myapp.querysets import ArticleQuerySet


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published().with_relations()
```

**`myapp/managers/__init__.py`**

```python
from myapp.managers.article_manager import ArticleManager

__all__ = ["ArticleManager"]
```

**`myapp/models/article.py`**

```python
from django.db import models
from django.urls import reverse

from myapp.managers import ArticleManager
from myapp.models.timestamped import TimeStampedModel


class Article(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="articles",
    )
    status = models.CharField(max_length=10, choices=Status, default=Status.DRAFT)
    tags = models.ManyToManyField("Tag", blank=True, related_name="articles")

    objects = ArticleManager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["status", "-created_at"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["author", "title"], name="unique_author_title"),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"pk": self.pk})
```

**`myapp/models/__init__.py`**

```python
from myapp.models.article import Article
from myapp.models.timestamped import TimeStampedModel

__all__ = ["Article", "TimeStampedModel"]
```

Key field options: `null`, `blank`, `choices`, `default`, `db_default` **[5.0+]**, `unique`, `db_index`, `help_text`, `verbose_name`.

Special field types:
- **GeneratedField** **[5.0+]**: Database-computed columns that are always derived from other fields.
- **CompositePrimaryKey** **[5.2+]**: Multi-column primary keys for complex schemas.

Relationships: `ForeignKey` (many-to-one), `ManyToManyField`, `OneToOneField`. **Always** set `related_name`.

For details, see [models-reference.md](references/models-reference.md).

### Views

Function-based or class-based. Return `HttpResponse` or raise an exception.

```python
# Function-based
from django.shortcuts import render, get_object_or_404

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, "myapp/article_detail.html", {"article": article})

# Class-based
from django.views.generic import ListView, DetailView, CreateView

class ArticleListView(ListView):
    model = Article
    paginate_by = 20

class ArticleDetailView(DetailView):
    model = Article
```

For details, see [views-reference.md](references/views-reference.md).

### URLs

Map URL patterns to views using `path()` and `re_path()`.

```python
from django.urls import path, include
from . import views

app_name = "myapp"

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="article-list"),
    path("<int:pk>/", views.ArticleDetailView.as_view(), name="article-detail"),
    path("create/", views.ArticleCreateView.as_view(), name="article-create"),
]
```

For details, see [urls-reference.md](references/urls-reference.md).

### Forms

```python
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "tags"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 10}),
        }
```

For details, see [forms-reference.md](references/forms-reference.md).

### Templates

Django template language uses `{{ variable }}`, `{% tag %}`, and `{{ value|filter }}`.

```html
{% extends "base.html" %}
{% load static %}

{% block content %}
<h1>{{ article.title }}</h1>
<p>By {{ article.author }} on {{ article.pub_date|date:"F j, Y" }}</p>
{{ article.content|linebreaks }}
{% endblock %}
```

### Admin

```python
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "pub_date"]
    list_filter = ["pub_date", "author"]
    search_fields = ["title", "content"]
    date_hierarchy = "pub_date"
```

For details, see [admin-reference.md](references/admin-reference.md).

## Version-Specific Features

### Django 5.0 Features

#### Field.db_default [5.0+]

Database-computed default values, evaluated by the database rather than Python.

```python
from django.db.models.functions import Now, Pi

class MyModel(models.Model):
    created = models.DateTimeField(db_default=Now())
    pi_value = models.FloatField(db_default=Pi())
```

#### GeneratedField [5.0+]

Database-generated columns (always computed from other fields). The value is computed by the database and cannot be set directly.

```python
from django.db.models import F

class Rectangle(models.Model):
    length = models.IntegerField()
    width = models.IntegerField()
    area = models.GeneratedField(
        expression=F("length") * F("width"),
        output_field=models.IntegerField(),
        db_persist=True,
    )
```

#### Simplified choices [5.0+]

Choices can now be a mapping (dict) or a flat iterable, in addition to the traditional list of 2-tuples or enums.

```python
# Mapping (dict) — keys are stored, values are display labels
status = models.CharField(max_length=10, choices={"draft": "Draft", "published": "Published"})

# Flat iterable — value is used as both the stored value and display label
color = models.CharField(max_length=10, choices=["red", "green", "blue"])
```

#### Admin Facet Filters [5.0+]

Show filter counts in the admin changelist using `show_facets`.

```python
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_filter = ["status", "author"]
    show_facets = admin.ShowFacets.ALWAYS
```

### Django 5.1 Features

#### LoginRequiredMiddleware [5.1+]

Global middleware that requires authentication for all views by default, removing the need for `@login_required` on every view.

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

Exempt specific views with the `login_not_required` decorator:

```python
from django.contrib.auth.decorators import login_not_required

@login_not_required
def public_view(request):
    ...

# For CBVs
from django.utils.decorators import method_decorator

@method_decorator(login_not_required, name="dispatch")
class PublicView(View):
    ...
```

#### querystring Template Tag [5.1+]

Build query strings easily in templates without manual URL encoding.

```html
{% load querystring %}

{# Add or replace query parameters #}
<a href="{% querystring page=2 %}">Page 2</a>

{# Preserve existing params and modify one #}
<a href="{% querystring page=page_obj.next_page_number %}">Next</a>
```

#### Connection Pooling for PostgreSQL [5.1+]

Built-in connection pooling for PostgreSQL (requires `psycopg[pool]` or `psycopg2`).

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mydb",
        "OPTIONS": {
            "pool": True,
        },
    }
}
```

### Django 5.2 Features

#### Composite Primary Keys [5.2+]

Support for composite primary keys using `CompositePrimaryKey`.

```python
from django.db import models

class Release(models.Model):
    pk = models.CompositePrimaryKey("version", "name")
    version = models.IntegerField()
    name = models.CharField(max_length=20)
```

#### Automatic Model Imports in Shell [5.2+]

The `manage.py shell` command automatically imports all models from installed apps.

```bash
$ python manage.py shell --verbosity=2

6 objects imported automatically, including:
  from django.contrib.auth.models import Group, Permission, User
  from django.contrib.contenttypes.models import ContentType
```

### Django 6.0 Features

#### Tasks Framework [6.0+]

Run code outside the request-response cycle. Define tasks with `@task` and enqueue them.

```python
from django.tasks import task

@task
def send_welcome_email(user_id):
    user = User.objects.get(pk=user_id)
    send_mail(subject="Welcome", message="...", from_email=None, recipient_list=[user.email])
    return True

# Enqueue
result = send_welcome_email.enqueue(user_id=42)
```

Configure backends in `TASKS` setting. Built-in: `ImmediateBackend` (default), `DummyBackend` (testing).

For details, see [tasks-reference.md](references/tasks-reference.md).

#### Content Security Policy [6.0+]

Built-in CSP middleware to mitigate XSS and control resource loading.

For details, see [security-reference.md](references/security-reference.md).

### Async Support (Mature, 5.0+)

Full async views, ORM queries (`async for`, `afirst()`, `acreate()`), and middleware support. Async ORM support was significantly expanded in Django 4.1–5.0 and is considered mature in 5.0+.

For details, see [async-reference.md](references/async-reference.md).

## Best Practices Summary

### Architecture
1. **Keep views thin** — views orchestrate, services execute, models encapsulate.
2. **Use a Service Layer** (`services.py`) for all business logic with `@transaction.atomic`.
3. **Models, QuerySets, and Managers MUST be packages** — each class in its own module (`models/article.py`, `querysets/article_query_set.py`, `managers/article_manager.py`), re-exported from `__init__.py`.
4. **Every model MUST have a Custom QuerySet and a Custom Manager** for reusable query logic (DRY).
5. **Use abstract base models** for shared fields (`TimeStampedModel`, `SoftDeleteModel`).
6. **Use mixins** for shared view/serializer behavior.

### Performance
6. **Always `select_related` / `prefetch_related`** — put in Custom QuerySet `with_relations()` method.
7. **Use `only()` / `defer()` / `values()`** when full model instances aren't needed.
8. **Use `bulk_create` / `bulk_update`** instead of looping `.save()`.
9. **Use `F()` expressions** for database-level field updates.
10. **Add `indexes`** in `Meta` for frequently filtered/sorted fields.
11. **Use `assertNumQueries()`** in tests to catch query regressions.

### Security
12. **Always use `{% csrf_token %}`** in POST forms.
13. **Always set `fields` explicitly** on ModelForm/Serializer — never `__all__`.
14. **Always check object-level permissions** before mutations.
15. **Never use `raw()` / `extra()` with string interpolation** — parameterize.
16. **Run `manage.py check --deploy`** before every deployment.
17. **Configure HTTPS, HSTS, CSP, secure cookies** in production.

### Migrations
18. **NEVER generate migration files from AI** — migrations MUST only be created via `python manage.py makemigrations`. The AI may instruct the user to run the command but MUST NOT write or edit migration files directly.
19. **Always commit migrations** to version control.
20. **Use `--check` in CI** to ensure no missing migrations.

### Code Quality
21. **Always define `__str__()`** on every model.
22. **Always define `get_absolute_url()`** on models with detail views.
23. **Always set `related_name`** on ForeignKey/M2M.
24. **Use `reverse()` / `{% url %}`** — never hardcode URLs.
25. **Use `TextChoices` / `IntegerChoices`** for all choice fields.
26. **Use `constraints`** instead of deprecated `unique_together`.
27. **Write tests** for models, views, forms, and services.

## Additional References

### Django core
- [Models Reference](references/models-reference.md)
- [Views Reference](references/views-reference.md)
- [Forms Reference](references/forms-reference.md)
- [URLs Reference](references/urls-reference.md)
- [Admin Reference](references/admin-reference.md)
- [Settings Reference](references/settings-reference.md)
- [Security Reference](references/security-reference.md)
- [Testing Reference](references/testing-reference.md)
- [Migrations Reference](references/migrations-reference.md)
- [Authentication Reference](references/auth-reference.md)
- [Async Reference](references/async-reference.md)
- [Tasks Reference](references/tasks-reference.md)
- [Middleware Reference](references/middleware-reference.md)
- [Templates Reference](references/templates-reference.md)
- [Common Patterns & Examples](examples.md)

### Third-party packages
- [Django REST Framework + SimpleJWT](references/drf-reference.md)
- [django-allauth](references/allauth-reference.md)
- [django-environ](references/environ-reference.md)
- [Celery](references/celery-reference.md)
- [Django Channels](references/channels-reference.md)
