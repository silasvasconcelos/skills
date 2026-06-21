---
name: django-unfold
description: >-
  Django Unfold admin theme — installation, UNFOLD settings, ModelAdmin options,
  filters, actions, tabs, inlines, widgets, dashboard components, third-party
  integrations, and troubleshooting. Use when styling Django admin with Unfold,
  configuring unfold.admin.ModelAdmin, UNFOLD dict, custom dashboards, or
  integrating django-import-export, simple-history, guardian, constance, hijack.
---

# Django Unfold Admin

Official docs: [unfoldadmin.com/docs](https://unfoldadmin.com/docs/) · Demo: [demo.unfoldadmin.com](https://demo.unfoldadmin.com) · Source examples: [github.com/unfoldadmin/formula](https://github.com/unfoldadmin/formula)

## Critical rules

1. **`unfold` before `django.contrib.admin`** in `INSTALLED_APPS`.
2. **Every admin class inherits `unfold.admin.ModelAdmin`**, not `django.contrib.admin.ModelAdmin`. Unstyled forms = wrong base class.
3. **Third-party admin classes** (User, import-export, etc.) must be unregistered and re-registered with Unfold `ModelAdmin`.
4. **Optional contrib apps** go immediately after `unfold`: `unfold.contrib.filters`, `.forms`, `.inlines`, etc.
5. **Production**: run `collectstatic`. Missing styles = static files not collected.
6. **Tailwind 3 custom CSS** incompatible with Unfold ≥ 0.56.0 — use Unfold's Tailwind setup or plain CSS.

## Quick start

```bash
pip install django-unfold
# or: uv add django-unfold / poetry add django-unfold
```

```python
# settings.py
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",   # optional
    "unfold.contrib.forms",     # optional
    "django.contrib.admin",
]
```

```python
# admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin

@admin.register(MyModel)
class MyModelAdmin(ModelAdmin):
    list_display = ["name"]
```

Copy full settings from [templates/settings-unfold.py.tpl](templates/settings-unfold.py.tpl).

## Workflows

### New Unfold admin setup

1. Install `django-unfold`, add `unfold` first in `INSTALLED_APPS`.
2. Add optional contrib apps matching your stack (see [references/integrations.md](references/integrations.md)).
3. Configure `UNFOLD` dict — site title, sidebar, colors (see [references/configuration.md](references/configuration.md)).
4. Change all `ModelAdmin` to inherit from `unfold.admin.ModelAdmin`.
5. Re-register User/Group with Unfold forms (see [references/installation.md](references/installation.md)).
6. Run `collectstatic` before deploy.

### Custom dashboard

1. Create `templates/admin/index.html` extending `admin/base.html`.
2. Set `UNFOLD["DASHBOARD_CALLBACK"]` to inject context variables.
3. Use `{% load unfold %}` and `{% component %}` tags (see [references/components.md](references/components.md)).
4. For custom Tailwind classes, compile project-level CSS (see [references/configuration.md](references/configuration.md#dashboard--tailwind)).

### Enhanced changelist

1. Add filters from `unfold.contrib.filters.admin` — set `list_filter_submit = True` for input filters.
2. Use `@display` decorator for labels, headers, dropdowns (see [references/configuration.md](references/configuration.md#display-decorator)).
3. Configure `actions_list`, `actions_row`, `actions_detail` with `@action` decorator (see [references/actions.md](references/actions.md)).
4. Optional: `list_sections` for expandable rows, `ordering_field` for drag-sort.

### Third-party package integration

Pattern: add `unfold.contrib.<package>` before the third-party app, inherit both mixins:

```python
from unfold.admin import ModelAdmin
from simple_history.admin import SimpleHistoryAdmin

class MyAdmin(SimpleHistoryAdmin, ModelAdmin):
    pass
```

Full matrix: [references/integrations.md](references/integrations.md).

## ModelAdmin cheat sheet

| Attribute | Purpose |
|-----------|---------|
| `compressed_fields` | Compact changeform layout (default True) |
| `warn_unsaved_form` | Warn on unsaved changes |
| `list_filter_submit` | Submit button for input filters |
| `list_filter_sheet` | False = sidebar filters |
| `list_fullwidth` | Full-width changelist |
| `actions_list` / `actions_row` / `actions_detail` / `actions_submit_line` | Custom actions |
| `list_sections` | Expandable changelist rows |
| `ordering_field` | Drag-sort changelist/inlines |
| `formfield_overrides` | WysiwygWidget, ArrayWidget |

Full list: [references/configuration.md](references/configuration.md#modeladmin-options).

## Filter types (require `unfold.contrib.filters`)

| Filter | Use case |
|--------|----------|
| `FieldTextFilter` | `__icontains` on field |
| `TextFilter` | Custom text query |
| `RangeDateFilter` / `RangeDateTimeFilter` | Date/datetime ranges |
| `ChoicesDropdownFilter` / `RelatedDropdownFilter` | Select dropdowns |
| `SingleNumericFilter` / `RangeNumericFilter` / `SliderNumericFilter` | Numeric ranges |

Details: [references/filters.md](references/filters.md).

## Action types

| Type | Attribute | Scope |
|------|-----------|-------|
| Global | `actions_list` | Model-wide, no queryset |
| Row | `actions_row` | Per row via dropdown |
| Detail | `actions_detail` | Changeform top |
| Submit line | `actions_submit_line` | Saves form first, then runs |

Use `@action` from `unfold.decorators` with `icon`, `variant`, `permissions`. Details: [references/actions.md](references/actions.md).

## References

| Topic | File |
|-------|------|
| Installation, auth, custom sites | [references/installation.md](references/installation.md) |
| UNFOLD settings, ModelAdmin, sections, sortable | [references/configuration.md](references/configuration.md) |
| Filters | [references/filters.md](references/filters.md) |
| Actions | [references/actions.md](references/actions.md) |
| Tabs, inlines, custom pages | [references/tabs-inlines.md](references/tabs-inlines.md) |
| Widgets & dashboard components | [references/widgets-components.md](references/widgets-components.md) |
| Third-party integrations | [references/integrations.md](references/integrations.md) |
| Troubleshooting & FAQ | [references/troubleshooting.md](references/troubleshooting.md) |
| End-to-end examples | [EXAMPLES.md](EXAMPLES.md) |

## Templates

| File | Purpose |
|------|---------|
| [templates/settings-unfold.py.tpl](templates/settings-unfold.py.tpl) | Full UNFOLD settings scaffold |
| [templates/admin-modeladmin.py.tpl](templates/admin-modeladmin.py.tpl) | Feature-rich ModelAdmin |
| [templates/admin-dashboard-index.html.tpl](templates/admin-dashboard-index.html.tpl) | Dashboard with components |
| [templates/admin-custom-page.py.tpl](templates/admin-custom-page.py.tpl) | Custom admin view |
| [templates/admin-custom-page.html.tpl](templates/admin-custom-page.html.tpl) | Custom page template |
| [templates/admin-user-group.py.tpl](templates/admin-user-group.py.tpl) | User/Group re-registration |
