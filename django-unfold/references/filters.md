# Filters

Source: [Introduction](https://unfoldadmin.com/docs/filters/introduction/) · Requires `unfold.contrib.filters` in `INSTALLED_APPS`.

## Setup

```python
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",  # immediately after unfold
    "django.contrib.admin",
]
```

Input-based filters need a submit button:

```python
class MyModelAdmin(ModelAdmin):
    list_filter_submit = True
```

## Filter options

```python
class MyModelAdmin(ModelAdmin):
    list_filter = ("category", "status")
    list_filter_options = {
        "category": {"label": "Category", "horizontal": True},
    }
```

## Text filters

```python
from django.core.validators import EMPTY_VALUES
from unfold.contrib.filters.admin import TextFilter, FieldTextFilter

class TitleFilter(TextFilter):
    title = "Title search"
    parameter_name = "title"

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(title__icontains=self.value())
        return queryset

class MyModelAdmin(ModelAdmin):
    list_filter_submit = True
    list_filter = [
        ("name", FieldTextFilter),  # auto __icontains on field
        TitleFilter,
    ]
```

## Datetime filters

```python
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter

class MyModelAdmin(ModelAdmin):
    list_filter_submit = True
    list_filter = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateTimeFilter),
    )
```

## Dropdown filters

All dropdowns use Select2. Avoid large datasets — no autocomplete.

```python
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    MultipleChoicesDropdownFilter,
    RelatedDropdownFilter,
    MultipleRelatedDropdownFilter,
    DropdownFilter,
)

class StatusFilter(DropdownFilter):
    title = "Status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [["active", "Active"], ["inactive", "Inactive"]]

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(status=self.value())
        return queryset

class MyModelAdmin(ModelAdmin):
    list_filter_submit = True
    list_filter = [
        StatusFilter,
        ("status", ChoicesDropdownFilter),
        ("tags", MultipleChoicesDropdownFilter),
        ("author", RelatedDropdownFilter),
        ("categories", MultipleRelatedDropdownFilter),
    ]
```

## Numeric filters

```python
from django.db.models import Count
from unfold.contrib.filters.admin import (
    RangeNumericListFilter,
    RangeNumericFilter,
    SingleNumericFilter,
    SliderNumericFilter,
)

class ItemCountFilter(RangeNumericListFilter):
    parameter_name = "items_count"
    title = "Items"

class MyModelAdmin(ModelAdmin):
    list_filter_submit = True
    list_filter = (
        ("price", SingleNumericFilter),       # __gte
        ("quantity", RangeNumericFilter),     # __gte and __lte
        ("score", SliderNumericFilter),
        ItemCountFilter,
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            items_count=Count("items", distinct=True)
        )
```

Custom slider: subclass `SliderNumericFilter` with `MAX_DECIMALS`, `STEP`.

## Filter layout

| Setting | Effect |
|---------|--------|
| `list_filter_sheet = True` | Filters in sheet/modal (default) |
| `list_filter_sheet = False` | Sidebar filters |
| `list_filter_submit = True` | Submit button for input filters |
| `list_filter_options[field]["horizontal"]` | Horizontal filter layout |
