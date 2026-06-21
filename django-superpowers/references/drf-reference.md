---
title: Django REST Framework + SimpleJWT Reference
---

# Django REST Framework + SimpleJWT Reference

Pinned: `djangorestframework~=3.17`, `djangorestframework-simplejwt~=5.5`.

## Install

```bash
pip install "djangorestframework~=3.17" "djangorestframework-simplejwt~=5.5"
```

Add to `core/settings.py`:

```python
INSTALLED_APPS = [
    # ...
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",  # required if rotation+blacklist
]
```

Run `python manage.py migrate` after adding the blacklist app.

## REST_FRAMEWORK settings

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
```

- **Never** set `fields = "__all__"` on `ModelSerializer` in production. Always enumerate.
- Add `SessionAuthentication` only on routes that need browsable API.

## SIMPLE_JWT settings

```python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env.str("DJANGO_JWT_SIGNING_KEY", default=SECRET_KEY),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}
```

Maintenance cron: `python manage.py flushexpiredtokens`.

## URL wiring

```python
# core/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
]
```

API calls: `Authorization: Bearer <access>`.

## Minimal ViewSet + Serializer + router

```python
# apps/items/serializers.py
from rest_framework import serializers

from apps.items.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "owner"]
        read_only_fields = ["owner"]


# apps/items/views.py
from rest_framework import viewsets

from apps.items.models import Item
from apps.items.serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# core/urls.py (fragment)
from rest_framework.routers import DefaultRouter
from django.urls import include, path

from apps.items.views import ItemViewSet

router = DefaultRouter()
router.register(r"items", ItemViewSet, basename="item")

urlpatterns += [path("api/", include(router.urls))]
```

## Shared DRF base classes

Put project-wide serializer/view bases in `core/serializers.py` and `core/views.py` so apps can extend them (DRY).

```python
# core/serializers.py
from rest_framework import serializers


class TimeStampedSerializerMixin(serializers.Serializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


# core/views.py
from rest_framework import viewsets


class OwnedModelViewSet(viewsets.ModelViewSet):
    """Restricts queryset to objects owned by request.user; sets owner on create."""

    owner_field = "owner"

    def get_queryset(self):
        return super().get_queryset().filter(**{self.owner_field: self.request.user})

    def perform_create(self, serializer):
        serializer.save(**{self.owner_field: self.request.user})
```

## SimpleJWT + django-allauth coexistence

See [allauth-reference.md](allauth-reference.md). Pick **one** token issuer per API. Default recommendation:

- **Allauth headless owns identity flows** (signup, verify, MFA, social).
- **SimpleJWT issues API tokens** via `/api/token/` once user has credentials.
- Do not authenticate the same API endpoint with both `JWTAuthentication` (SimpleJWT) and `JWTTokenAuthentication` (allauth headless).
