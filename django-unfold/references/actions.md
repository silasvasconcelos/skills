# Actions

Source: [Introduction](https://unfoldadmin.com/docs/actions/introduction/) · Based on Django admin actions with Unfold enhancements.

## Overview

| Type | Attribute | Location | Receives |
|------|-----------|----------|----------|
| Global | `actions_list` | Changelist top | `request` only |
| Row | `actions_row` | Each row dropdown | `request`, `object_id` |
| Detail | `actions_detail` | Changeform top | `request`, `object_id` |
| Submit line | `actions_submit_line` | Near Save button | `request`, `obj` (saved) |

## Basic action

```python
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import action
from unfold.enums import ActionVariant

class MyModelAdmin(ModelAdmin):
    actions_list = ["export_all"]
    actions_row = ["duplicate_row"]
    actions_detail = ["archive_object"]
    actions_submit_line = ["save_and_notify"]

    @action(description=_("Export all"), icon="download", variant=ActionVariant.PRIMARY)
    def export_all(self, request: HttpRequest):
        # No queryset — model-wide operation
        return redirect(reverse_lazy("admin:app_mymodel_changelist"))

    @action(
        description=_("Duplicate"),
        icon="content_copy",
        url_path="duplicate",
        permissions=["duplicate_row"],
        attrs={"target": "_blank"},
    )
    def duplicate_row(self, request: HttpRequest, object_id: int):
        return redirect(reverse_lazy("admin:app_mymodel_change", args=(object_id,)))

    @action(description=_("Archive"), icon="archive", permissions=["archive_object"])
    def archive_object(self, request: HttpRequest, object_id: int):
        obj = self.model.objects.get(pk=object_id)
        obj.is_archived = True
        obj.save()
        return redirect(reverse_lazy("admin:app_mymodel_change", args=(object_id,)))

    @action(description=_("Save & notify"), permissions=["save_and_notify"])
    def save_and_notify(self, request: HttpRequest, obj):
        # Form already saved — obj is persisted
        send_notification(obj)
        obj.notified = True
        obj.save()
```

## Permissions

Two permission systems:

1. **Django built-in**: `"app_label.permission_codename"` in `permissions` list
2. **ModelAdmin method**: `has_{action_name}_permission(self, request, obj=None)`

```python
class MyModelAdmin(ModelAdmin):
    @action(
        description="Custom action",
        permissions=["custom_action", "app.view_mymodel"],
    )
    def custom_action(self, request, object_id: int):
        pass

    def has_custom_action_permission(self, request, obj=None):
        return request.user.is_superuser
```

Note: Django built-in permissions (with dot) do not receive `obj` on detail view checks.

Row actions: permissions are global — no per-row permission via `object_id`.

## Icons and variants

```python
from unfold.enums import ActionVariant

@action(description="Approve", icon="check", variant=ActionVariant.SUCCESS)
def approve(self, request, object_id: int):
    ...
```

Variants: `DEFAULT`, `PRIMARY`, `SUCCESS`, `INFO`, `WARNING`, `DANGER`.

Icons use [Google Material Symbols](https://fonts.google.com/icons) names.

## Hide built-in actions

```python
class MyModelAdmin(ModelAdmin):
    actions_list = ["my_action", "history_wrapper"]
    actions_list_hide_default = True
    actions_detail_hide_default = True

    @action(description="History", icon="history")
    def history_wrapper(self, request, object_id: int):
        return redirect("admin:app_mymodel_history", object_id)
```

## Multi-step actions

For forms or confirmation pages, redirect from the action handler to a custom view extending Unfold base views:

```python
@action(description="Bulk import", url_path="bulk-import")
def bulk_import(self, request):
    return redirect("admin:app_mymodel_bulk_import")
```

Register custom URL in `get_urls()` with `self.admin_site.admin_view()`.

## Submit line behavior

`actions_submit_line` saves the form first (like clicking Save), then runs action logic. The `obj` argument is already persisted — save again if you modify it.

## Dropdown action groups

Group related actions under one dropdown by configuring multiple actions — Unfold renders them in action dropdowns on changelist/changeform. Use `actions_list_hide_default` to consolidate built-in actions into custom dropdown wrappers.