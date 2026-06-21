# Third-Party Integrations

Pattern for all integrations:
1. Add `unfold.contrib.<package>` **after** `unfold`, **before** the third-party app
2. Inherit from **both** the third-party admin mixin and `unfold.admin.ModelAdmin`

## Integration matrix

| Package | Contrib app | Admin mixin | Notes |
|---------|-------------|-------------|-------|
| django-import-export | `unfold.contrib.import_export` | `ImportExportModelAdmin` | Set `ImportForm`, `ExportForm` |
| django-simple-history | `unfold.contrib.simple_history` | `SimpleHistoryAdmin` | Dual inheritance |
| django-guardian | `unfold.contrib.guardian` | — | Adds "Object permissions" button |
| django-constance | `unfold.contrib.constance` | — | Template overrides |
| django-hijack | `unfold.contrib.hijack` | — | Hijack button styling |
| django-celery-beat | — | — | See [integration docs](https://unfoldadmin.com/docs/integrations/django-celery-beat/) |
| djangoql | — | — | See [integration docs](https://unfoldadmin.com/docs/integrations/djangoql/) |
| django-money | — | — | See [integration docs](https://unfoldadmin.com/docs/integrations/django-money/) |
| django-json-widget | — | — | See [integration docs](https://unfoldadmin.com/docs/integrations/django-json-widget/) |
| django-modeltranslation | — | `EXTENSIONS` in UNFOLD | Flag config in settings |
| django-location-field | `unfold.contrib.location_field` | — | Map widget styling |

## django-import-export

```python
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.import_export",
    "import_export",
]

from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

class ProductAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
```

django-import-export 4.x+: default `ExportActionModelAdmin` styling fixed — custom Unfold wrapper removed.

Demo: [demo.unfoldadmin.com/formula/constructor](https://demo.unfoldadmin.com/en/admin/formula/constructor/)

## django-simple-history

```python
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.simple_history",
    "simple_history",
]

from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin

class ProductAdmin(SimpleHistoryAdmin, ModelAdmin):
    pass
```

## django-guardian

```python
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.guardian",
    "guardian",
]
```

Adds "Object permissions" button on changeform detail page.

## django-constance

```python
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.constance",
    "constance",
]
```

## django-hijack

```python
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.hijack",
    "hijack",
]
```

## django-location-field

```python
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.location_field",
    "location_field",
]
```

## django-modeltranslation

Configure flags in UNFOLD:

```python
UNFOLD = {
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {"en": "🇬🇧", "pt": "🇧🇷"},
        },
    },
}
```

## Re-registering third-party admins

When a package auto-registers with default `ModelAdmin`:

```python
from third_party.admin import SomeAdmin as BaseSomeAdmin
from third_party.models import SomeModel
from unfold.admin import ModelAdmin

admin.site.unregister(SomeModel)

@admin.register(SomeModel)
class SomeAdmin(BaseSomeAdmin, ModelAdmin):
    pass
```

MRO: third-party mixin first, `ModelAdmin` last (unless docs say otherwise).

## Consulting for unsupported packages

Unfold does not style all third-party admin packages. For business-critical packages without integration, see [Unfold Consulting](https://unfoldadmin.com/consulting/).
