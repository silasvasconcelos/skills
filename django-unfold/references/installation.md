# Installation & Setup

Source: [Quickstart](https://unfoldadmin.com/docs/installation/quickstart/) · [User & group models](https://unfoldadmin.com/docs/installation/auth/) · [Custom sites](https://unfoldadmin.com/docs/configuration/custom-sites/)

## Install

```bash
pip install django-unfold
uv add django-unfold
poetry add django-unfold
```

## INSTALLED_APPS order

```python
INSTALLED_APPS = [
    "unfold",                          # MUST be before django.contrib.admin
    "unfold.contrib.filters",          # optional — enhanced filters
    "unfold.contrib.forms",            # optional — WysiwygWidget, ArrayWidget
    "unfold.contrib.inlines",          # optional — Nonrelated inlines
    "unfold.contrib.import_export",    # optional — django-import-export
    "unfold.contrib.guardian",         # optional — django-guardian
    "unfold.contrib.simple_history",   # optional — django-simple-history
    "unfold.contrib.location_field",   # optional — django-location-field
    "unfold.contrib.constance",        # optional — django-constance
    "unfold.contrib.hijack",           # optional — django-hijack
    "django.contrib.admin",
    # ... other apps
]
```

Contrib apps must appear **immediately after** `unfold`.

## URLs

Default admin URLs work unchanged:

```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]
```

## ModelAdmin inheritance

```python
from unfold.admin import ModelAdmin  # NOT django.contrib.admin.ModelAdmin

@admin.register(MyModel)
class MyModelAdmin(ModelAdmin):
    pass
```

## User & Group models

Django's default User/Group admin uses `django.contrib.admin.ModelAdmin` → unstyled. Unregister and re-register:

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
```

For custom user model, same pattern with your project's `UserAdmin` base.

## Third-party admin re-registration

Any package registering admin with default `ModelAdmin` needs the same unregister/re-register pattern:

```python
from some_package.admin import SomeModelAdmin as BaseSomeAdmin
from some_package.models import SomeModel
from unfold.admin import ModelAdmin

admin.site.unregister(SomeModel)

@admin.register(SomeModel)
class SomeModelAdmin(BaseSomeAdmin, ModelAdmin):
    pass
```

**MRO note**: Put Unfold `ModelAdmin` last in the inheritance list unless docs specify otherwise.

## Custom admin site

Use `UnfoldAdminSite` — default `AdminSite` causes `NoReverseMatch`:

```python
# sites.py
from unfold.sites import UnfoldAdminSite

class CustomAdminSite(UnfoldAdminSite):
    pass

custom_admin_site = CustomAdminSite(name="custom_admin_site")
```

```python
# urls.py
from .sites import custom_admin_site

urlpatterns = [
    path("admin/", custom_admin_site.urls),
]
```

```python
# admin.py — register with site=
@admin.register(MyModel, site=custom_admin_site)
class MyModelAdmin(ModelAdmin):
    pass
```

### Override default admin site

Use `unfold.apps.BasicAppConfig` (not bare `"unfold"`) when overriding via `AdminConfig`:

```python
# settings.py
INSTALLED_APPS = [
    "unfold.apps.BasicAppConfig",
    "django.contrib.admin",
    "your_app",
]

# apps.py
from django.contrib.admin.apps import AdminConfig

class MyAdminConfig(AdminConfig):
    default_site = "myproject.sites.CustomAdminSite"
```

## Deployment checklist

- [ ] `unfold` before `django.contrib.admin`
- [ ] All ModelAdmin inherit from `unfold.admin.ModelAdmin`
- [ ] User/Group re-registered with Unfold forms
- [ ] `python manage.py collectstatic` run
- [ ] `TEMPLATES['DIRS']` includes project templates dir (for custom dashboard)
- [ ] Third-party integrations use matching `unfold.contrib.*` apps
