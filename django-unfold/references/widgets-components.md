# Widgets & Dashboard Components

Sources: [WysiwygWidget](https://unfoldadmin.com/docs/widgets/wysiwyg/) · [ArrayWidget](https://unfoldadmin.com/docs/widgets/array/) · [Components](https://unfoldadmin.com/docs/components/introduction/)

## Setup

```python
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.forms",
]
```

## WysiwygWidget

Trix-based rich text editor for `TextField`:

```python
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

class ArticleAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
    }
```

No built-in file upload — upload media separately, insert URL in editor.

## ArrayWidget

For PostgreSQL `ArrayField`:

```python
from django.contrib.postgres.fields import ArrayField
from django.db.models import TextChoices
from unfold.contrib.forms.widgets import ArrayWidget

class TagChoices(TextChoices):
    NEWS = "news", "News"
    SPORT = "sport", "Sport"

class ArticleAdmin(ModelAdmin):
    formfield_overrides = {
        ArrayField: {"widget": ArrayWidget},
    }

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["tags"].widget = ArrayWidget(choices=TagChoices)
        return form
```

With `choices`, renders dropdown; without, text input per item.

## Dashboard components

Load in templates with `{% load unfold %}`.

### Available components

| Component | Path | Key args |
|-----------|------|----------|
| Container | `unfold/components/container.html` | `class` |
| Card | `unfold/components/card.html` | `class`, `title`, `footer`, `label`, `icon` |
| Title | `unfold/components/title.html` | `class` |
| Text | `unfold/components/text.html` | `class` |
| Button | `unfold/components/button.html` | `class`, `name`, `href`, `submit` |
| Table | `unfold/components/table.html` | `table`, `card_included`, `striped` |
| Chart (bar) | `unfold/components/chart/bar.html` | `data`, `height`, `width` |
| Chart (line) | `unfold/components/chart/line.html` | `data`, `height`, `width` |
| Progress | `unfold/components/progress.html` | `value`, `title`, `description` |
| Navigation | `unfold/components/navigation.html` | `items` |
| Tracker | `unfold/components/tracker.html` | `data` |
| Cohort | `unfold/components/cohort.html` | `data` |
| Layer | `unfold/components/layer.html` | wraps nested components |

### Nesting

```html
{% load i18n unfold %}

{% block content %}
{% component "unfold/components/container.html" %}
    <div class="grid grid-cols-3 gap-4">
        {% for card in cards %}
            {% component "unfold/components/card.html" %}
                {% component "unfold/components/text.html" %}
                    {{ card.title }}
                {% endcomponent %}
                {% component "unfold/components/title.html" %}
                    {{ card.metric }}
                {% endcomponent %}
            {% endcomponent %}
        {% endfor %}
    </div>
{% endcomponent %}
{% endblock %}
```

Components support `children` and params via `{% component "path" with param=value %}`.

## DASHBOARD_CALLBACK

```python
# callbacks.py
def dashboard_callback(request, context):
    context.update({
        "cards": [
            {"title": "Users", "metric": "1,234"},
            {"title": "Orders", "metric": "567"},
        ],
        "navigation": [
            {"title": "All orders", "link": "/admin/orders/order/"},
        ],
    })
    return context
```

```python
# settings.py
UNFOLD = {
    "DASHBOARD_CALLBACK": "myapp.callbacks.dashboard_callback",
}
```

Reference implementation: [github.com/unfoldadmin/formula](https://github.com/unfoldadmin/formula)
