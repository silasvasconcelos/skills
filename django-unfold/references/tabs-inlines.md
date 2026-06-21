# Tabs, Inlines & Custom Pages

Sources: [Changelist tabs](https://unfoldadmin.com/docs/tabs/changelist/) · [Changeform tabs](https://unfoldadmin.com/docs/tabs/changeform/) · [Inlines](https://unfoldadmin.com/docs/inlines/introduction/) · [Custom pages](https://unfoldadmin.com/docs/configuration/custom-pages/)

## Changelist tabs

Configure in `UNFOLD["TABS"]`:

```python
UNFOLD = {
    "TABS": [
        {
            "models": ["orders.order", "orders.shipment"],
            "items": [
                {
                    "title": _("Orders"),
                    "link": reverse_lazy("admin:orders_order_changelist"),
                    "permission": "myapp.tabs.permission_callback",
                },
                {
                    "title": _("Shipments"),
                    "link": reverse_lazy("admin:orders_shipment_changelist"),
                },
            ],
        },
    ],
}
```

## Changeform tabs

Same structure; models need `detail: True`:

```python
"models": [
    {"name": "orders.order", "detail": True},
],
```

## Fieldsets & inline tabs

Fieldsets tabs and inline tabs are configured on `ModelAdmin` using Unfold tab helpers — group fieldsets or inlines into tabbed sections on the changeform. See [Fieldsets tabs](https://unfoldadmin.com/docs/tabs/fieldsets/) and [Inlines tabs](https://unfoldadmin.com/docs/tabs/inlines/) for model-specific syntax.

Dynamic tabs: generated at runtime based on model state — see [Dynamic tabs](https://unfoldadmin.com/docs/tabs/dynamic/).

## Inlines

Use Unfold inline classes for consistent styling:

```python
from unfold.admin import ModelAdmin, StackedInline, TabularInline

class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(ModelAdmin):
    inlines = [OrderItemInline]
```

Django's native `StackedInline`/`TabularInline` work but look unstyled.

Requires `unfold.contrib.inlines` for nonrelated inlines:

```python
from unfold.contrib.inlines.admin import NonrelatedStackedInline, NonrelatedTabularInline
```

## Sortable inlines

```python
class ItemInline(TabularInline):
    model = Item
    ordering_field = "weight"
    hide_ordering_field = True
    list_display = ["name", "weight"]
```

Model field: `PositiveIntegerField(default=0, db_index=True)`. New inline rows must be saved before reordering.

## Paginated inlines

```python
class ItemInline(TabularInline):
    model = Item
    per_page = 10
```

Works with StackedInline, TabularInline, Generic*, and Nonrelated* inlines. No AJAX — full page reload. Hidden when records fit on one page.

## Custom admin pages

```python
from django.urls import path
from django.views.generic import TemplateView
from unfold.admin import ModelAdmin
from unfold.views import UnfoldModelAdminViewMixin

class ReportView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Sales Report"
    permission_required = ("orders.view_order",)
    template_name = "admin/orders/report.html"

class OrderAdmin(ModelAdmin):
    def get_urls(self):
        custom = self.admin_site.admin_view(
            ReportView.as_view(model_admin=self)
        )
        return super().get_urls() + [
            path("report/", custom, name="orders_order_report"),
        ]
```

Template:

```html
{% extends "admin/base.html" %}
{% load i18n unfold %}

{% block content %}
    {% tab_list "orders" %}
    <h1>{% trans "Sales Report" %}</h1>
{% endblock %}
```

Add custom views to `UNFOLD["SIDEBAR"]["navigation"]` manually — not auto-linked.

## Conditional fields

Show/hide fields based on other field values on the changeform. Configure via `conditional_fields` on `ModelAdmin` — see [Conditional fields](https://unfoldadmin.com/docs/configuration/conditional-fields/).
