# Troubleshooting & FAQ

Source: [Unfold docs FAQ](https://unfoldadmin.com/docs/)

## Site completely unstyled

**Causes:**
1. `collectstatic` not run in production
2. Custom Tailwind 3 CSS file included — incompatible with Unfold ≥ 0.56.0

**Fix:**
```bash
python manage.py collectstatic --noinput
```

Remove or replace project Tailwind 3 output. Use Unfold's project-level Tailwind setup or plain CSS via `UNFOLD["STYLES"]`.

## Form fields unstyled

**Cause:** ModelAdmin inherits `django.contrib.admin.ModelAdmin` instead of `unfold.admin.ModelAdmin`.

**Fix:**
```python
from unfold.admin import ModelAdmin  # correct

class MyAdmin(ModelAdmin):
    pass
```

## User/Group forms not styled

**Cause:** Default Django auth admin not re-registered.

**Fix:** Unregister User/Group, re-register with `BaseUserAdmin, ModelAdmin` and Unfold forms (`UserChangeForm`, `UserCreationForm`, `AdminPasswordChangeForm`). See [installation.md](installation.md).

## Third-party package unstyled

**Cause:** Package registers admin with default `ModelAdmin`.

**Fix:** Unregister and re-register with `unfold.admin.ModelAdmin`. Add matching `unfold.contrib.*` app if available. See [integrations.md](integrations.md).

## NoReverseMatch with custom admin site

**Cause:** Using `django.contrib.admin.AdminSite` instead of `UnfoldAdminSite`.

**Fix:**
```python
from unfold.sites import UnfoldAdminSite
custom_admin_site = UnfoldAdminSite(name="custom_admin_site")
```

## Filters not submitting

**Cause:** Input filters need explicit submit.

**Fix:** `list_filter_submit = True` on ModelAdmin.

## Dropdown filter performance

**Cause:** Select2 dropdowns load all options — no autocomplete.

**Fix:** Use text filters or autocomplete fields for large datasets. Do not use dropdown filters on FK fields with thousands of rows.

## list_sections N+1 queries

**Cause:** 100 records/page × related table queries per row.

**Fix:**
- Reduce `list_per_page = 20`
- Override `get_queryset` with `prefetch_related` for all `list_sections` related names
- Use django-debug-toolbar to verify

## Sortable inlines/changelist not working

**Checks:**
- Field is `PositiveIntegerField(default=0, db_index=True)`
- `ordering_field` set on ModelAdmin/Inline
- For inlines: new rows must be saved before drag-sort
- Changelist sort: only within current page

## Custom dashboard styles missing

**Cause:** Tailwind classes in custom `templates/admin/index.html` not compiled.

**Fix:** Set up project-level Tailwind compilation per Unfold docs, or use inline CSS / `UNFOLD["STYLES"]`.

## Submit line action not seeing form data

**Cause:** Misunderstanding submit line flow.

**Note:** `actions_submit_line` saves form first, then passes saved `obj`. Modify and `.save()` again if needed.

## Row action permissions

**Limitation:** Row actions cannot vary permission per row — `has_*_permission` has no `object_id`.

## Demo & reference project

- Live demo: [demo.unfoldadmin.com](https://demo.unfoldadmin.com)
- Full examples: [github.com/unfoldadmin/formula](https://github.com/unfoldadmin/formula)
- Turbo boilerplate (Django + Next.js): [github.com/unfoldadmin/turbo](https://github.com/unfoldadmin/turbo)
