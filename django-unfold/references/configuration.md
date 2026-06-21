# Configuration

Source: [Settings options](https://unfoldadmin.com/docs/configuration/settings/) · [ModelAdmin options](https://unfoldadmin.com/docs/configuration/modeladmin/) · [Dashboard](https://unfoldadmin.com/docs/configuration/dashboard/) · [Sections](https://unfoldadmin.com/docs/configuration/sections/) · [Sortable changelist](https://unfoldadmin.com/docs/configuration/sortable-changelist/) · [Display decorator](https://unfoldadmin.com/docs/decorators/display/)

## UNFOLD settings dict

All customization lives in `settings.py`:

```python
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "My Admin",
    "SITE_HEADER": "My Admin",
    "SITE_SUBHEADER": "Management panel",
    "SITE_URL": "/",
    "SITE_SYMBOL": "speed",  # Google Material icon name
    "SITE_ICON": {
        "light": lambda request: static("icon-light.svg"),
        "dark": lambda request: static("icon-dark.svg"),
    },
    "SITE_LOGO": {
        "light": lambda request: static("logo-light.svg"),
        "dark": lambda request: static("logo-dark.svg"),
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("favicon.svg"),
        },
    ],
    "SITE_DROPDOWN": [
        {"icon": "diamond", "title": _("External"), "link": "https://example.com"},
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": False,
    "SHOW_UI_WARNINGS": False,
    "THEME": None,  # "dark" | "light" to force; None = user switcher
    "BORDER_RADIUS": "6px",
    "ENVIRONMENT": "myapp.callbacks.environment_callback",
    "ENVIRONMENT_TITLE_PREFIX": "myapp.callbacks.environment_title_prefix_callback",
    "DASHBOARD_CALLBACK": "myapp.callbacks.dashboard_callback",
    "STYLES": [lambda request: static("css/admin-custom.css")],
    "SCRIPTS": [lambda request: static("js/admin-custom.js")],
    "LOGIN": {
        "image": lambda request: static("login-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:index"),
        "form": "myapp.forms.CustomLoginForm",
    },
    "COLORS": {
        "base": {"50": "oklch(...)", "950": "oklch(...)"},
        "primary": {"50": "oklch(...)", "950": "oklch(...)"},
        "font": {
            "subtle-light": "var(--color-base-500)",
            "default-dark": "var(--color-base-300)",
            "important-light": "var(--color-base-900)",
        },
    },
    "SIDEBAR": {
        "show_search": False,
        "command_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                        "badge": "myapp.callbacks.badge_callback",
                        "badge_variant": "info",
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
        ],
    },
    "TABS": [
        {
            "models": ["app_label.modelname"],
            "items": [
                {
                    "title": _("Tab title"),
                    "link": reverse_lazy("admin:app_model_changelist"),
                    "permission": "myapp.callbacks.permission_callback",
                },
            ],
        },
    ],
    "EXTENSIONS": {
        "modeltranslation": {"flags": {"en": "🇬🇧", "pt": "🇧🇷"}},
    },
}
```

### Callback signatures

```python
def dashboard_callback(request, context):
    context.update({"metric_count": 42})
    return context

def environment_callback(request):
    return ["Production", "danger"]  # text, variant: info|danger|warning|success

def badge_callback(request):
    return 3  # int displayed as badge

def permission_callback(request):
    return request.user.has_perm("app.change_model")
```

## ModelAdmin options

```python
from django.db import models
from django.contrib.postgres.fields import ArrayField
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget

class MyModelAdmin(ModelAdmin):
    show_add_link = True
    compressed_fields = True
    warn_unsaved_form = True
    readonly_preprocess_fields = {
        "html_field": "html.unescape",
        "other_field": lambda content: content.strip(),
    }
    list_filter_submit = False
    list_filter_options = {
        "status": {"label": "Status", "horizontal": True},
    }
    list_fullwidth = False
    list_filter_sheet = True          # False = sidebar filters
    list_horizontal_scrollbar_top = False
    list_disable_select_all = False
    list_per_page = 25

    # Actions (see actions.md)
    actions_list = []
    actions_row = []
    actions_detail = []
    actions_submit_line = []
    actions_list_hide_default = False
    actions_detail_hide_default = False

    # Changeform templates
    change_form_before_template = None
    change_form_after_template = None
    change_form_outer_before_template = None
    change_form_outer_after_template = None
    change_form_show_cancel_button = True

    # Sortable changelist
    ordering_field = "weight"
    hide_ordering_field = True

    # Expandable rows
    list_sections = []

    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
        ArrayField: {"widget": ArrayWidget},
    }
```

Requires `PositiveIntegerField(default=0, db_index=True)` on model for `ordering_field`.

## Display decorator

```python
from unfold.decorators import display

class MyModelAdmin(ModelAdmin):
    list_display = ["show_status", "show_user_header", "show_dropdown"]

    @display(description="Status", ordering="status", label=True)
    def show_status(self, obj):
        return obj.status

    @display(
        description="Status",
        ordering="status",
        label={"active": "success", "pending": "info", "cancelled": "danger"},
    )
    def show_status_colored(self, obj):
        return obj.status

    @display(header=True)
    def show_user_header(self, obj):
        return ["John Doe", "john@example.com", "JD"]

    @display(description="Actions", dropdown=True)
    def show_dropdown(self, obj):
        return {
            "title": "Options",
            "striped": True,
            "height": 200,
            "width": 240,
            "items": [
                {"title": "Edit", "link": f"/admin/app/model/{obj.pk}/change/"},
                {"title": "View site", "link": obj.get_absolute_url()},
            ],
        }
```

Label colors: `success`, `info`, `warning`, `danger`, `primary`.

Header format: `[main_heading, subtitle, initials_or_badge, optional_image_dict]`.

## Sections (expandable changelist rows)

```python
from unfold.sections import TableSection, TemplateSection

class RelatedTableSection(TableSection):
    verbose_name = "Related items"
    height = 300
    related_name = "items"
    fields = ["pk", "title"]

    def custom_field(self, instance):
        return instance.pk

class CardSection(TemplateSection):
    template_name = "myapp/admin/section_card.html"

class MyModelAdmin(ModelAdmin):
    list_sections = [RelatedTableSection, CardSection]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("items")
```

Optimize with `prefetch_related` — default 100 records/page causes N+1 without it.

## Dashboard & Tailwind

1. Add `BASE_DIR / "templates"` to `TEMPLATES['DIRS']`.
2. Create `templates/admin/index.html` extending `admin/base.html`.
3. Set `DASHBOARD_CALLBACK` to inject variables.
4. Custom Tailwind classes require project-level Tailwind compilation — they are NOT bundled in Unfold.
5. Do NOT include incompatible Tailwind 3 generated CSS (breaks Unfold ≥ 0.56.0).

Minimal dashboard template:

```html
{% extends "admin/base.html" %}
{% load i18n unfold %}

{% block content %}
    {% component "unfold/components/container.html" %}
        <p>{{ custom_variable }}</p>
    {% endcomponent %}
{% endblock %}
```

## Sortable changelist

Model:

```python
class MyModel(models.Model):
    weight = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ["weight"]
```

Admin: `ordering_field = "weight"`, `hide_ordering_field = True`.

Limitation: sorting only within current page (pagination).
