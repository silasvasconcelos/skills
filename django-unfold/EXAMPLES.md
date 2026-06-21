# Django Unfold — Examples

End-to-end patterns. Copy and adapt to your project.

---

## 1. Minimal setup

**settings.py**

```python
INSTALLED_APPS = [
    "unfold",
    "django.contrib.admin",
    "myapp",
]
```

**admin.py**

```python
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Product

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ["name", "price", "created_at"]
    search_fields = ["name"]
```

---

## 2. Full-featured ModelAdmin

```python
from django.contrib import admin
from django.db import models
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import action, display
from unfold.contrib.filters.admin import (
    FieldTextFilter,
    RangeDateFilter,
    ChoicesDropdownFilter,
)
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.enums import ActionVariant
from .models import Article

@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ["title_display", "author", "status_display", "published_at"]
    list_filter_submit = True
    list_filter = [
        ("title", FieldTextFilter),
        ("status", ChoicesDropdownFilter),
        ("published_at", RangeDateFilter),
    ]
    search_fields = ["title", "body"]
    compressed_fields = True
    warn_unsaved_form = True
    actions_list = ["publish_all_drafts"]
    actions_row = ["preview"]
    actions_detail = ["publish"]
    ordering_field = "weight"
    hide_ordering_field = True

    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
    }

    @display(description=_("Title"), header=True)
    def title_display(self, obj):
        return [obj.title, obj.slug, obj.title[:2].upper()]

    @display(description=_("Status"), label={"draft": "warning", "published": "success"})
    def status_display(self, obj):
        return obj.status

    @action(description=_("Publish all drafts"), icon="publish", variant=ActionVariant.PRIMARY)
    def publish_all_drafts(self, request):
        self.model.objects.filter(status="draft").update(status="published")
        self.message_user(request, "Drafts published.")
        return redirect("admin:myapp_article_changelist")

    @action(description=_("Preview"), icon="visibility", permissions=["preview"])
    def preview(self, request, object_id: int):
        return redirect(f"/articles/{object_id}/")

    @action(description=_("Publish"), icon="check")
    def publish(self, request, object_id: int):
        obj = self.model.objects.get(pk=object_id)
        obj.status = "published"
        obj.save()
        return redirect("admin:myapp_article_change", object_id)

    def has_preview_permission(self, request, obj=None):
        return request.user.has_perm("myapp.view_article")
```

---

## 3. Custom dashboard with components

**callbacks.py**

```python
def dashboard_callback(request, context):
    from myapp.models import Order, User

    context.update({
        "cards": [
            {"title": "Total orders", "metric": Order.objects.count()},
            {"title": "Active users", "metric": User.objects.filter(is_active=True).count()},
        ],
    })
    return context
```

**settings.py**

```python
UNFOLD = {"DASHBOARD_CALLBACK": "myapp.callbacks.dashboard_callback"}
```

**templates/admin/index.html**

```html
{% extends "admin/base.html" %}
{% load i18n unfold %}

{% block content %}
{% component "unfold/components/container.html" %}
    <div class="grid grid-cols-2 gap-4 mb-8">
        {% for card in cards %}
            {% component "unfold/components/card.html" %}
                {% component "unfold/components/text.html" %}{{ card.title }}{% endcomponent %}
                {% component "unfold/components/title.html" %}{{ card.metric }}{% endcomponent %}
            {% endcomponent %}
        {% endfor %}
    </div>
{% endcomponent %}
{% endblock %}
```

---

## 4. User & Group admin

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
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

---

## 5. django-import-export

```python
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.import_export",
    "import_export",
    "myapp",
]

from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

@admin.register(Product)
class ProductAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ["sku", "name", "price"]
```

---

## 6. Custom text filter + row action

```python
from django.core.validators import EMPTY_VALUES
from django.shortcuts import redirect
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import TextFilter
from unfold.decorators import action

class EmailDomainFilter(TextFilter):
    title = "Email domain"
    parameter_name = "domain"

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(email__endswith=f"@{self.value()}")
        return queryset

@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_filter_submit = True
    list_filter = [EmailDomainFilter]
    actions_row = ["send_welcome"]

    @action(description="Send welcome email", icon="mail")
    def send_welcome(self, request, object_id: int):
        customer = self.model.objects.get(pk=object_id)
        send_welcome_email(customer)
        self.message_user(request, f"Welcome email sent to {customer.email}")
        return redirect("admin:myapp_customer_changelist")
```

---

## 7. Expandable changelist sections

```python
from unfold.admin import ModelAdmin
from unfold.sections import TableSection

class OrderItemsSection(TableSection):
    verbose_name = "Order items"
    related_name = "items"
    fields = ["product", "quantity", "price"]

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_sections = [OrderItemsSection]
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("items")
```

---

## 8. Custom admin page

See [templates/admin-custom-page.py.tpl](templates/admin-custom-page.py.tpl) and [templates/admin-custom-page.html.tpl](templates/admin-custom-page.html.tpl).
