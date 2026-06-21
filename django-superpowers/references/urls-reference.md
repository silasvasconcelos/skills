# Django URLs Reference (5.0+)

## URL Configuration

```python
# project/urls.py (root URLconf)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("articles/", include("articles.urls")),
    path("api/", include("api.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

```python
# app/urls.py
from django.urls import path
from . import views

app_name = "articles"  # application namespace

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="list"),
    path("<int:pk>/", views.ArticleDetailView.as_view(), name="detail"),
    path("<slug:slug>/", views.article_by_slug, name="detail-by-slug"),
    path("create/", views.ArticleCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.ArticleUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.ArticleDeleteView.as_view(), name="delete"),
]
```

## Path Converters

| Converter | Matches | Returns |
|-----------|---------|---------|
| `str` | Any non-empty string except `/` (default) | `str` |
| `int` | Zero or positive integer | `int` |
| `slug` | ASCII letters, numbers, hyphens, underscores | `str` |
| `uuid` | Formatted UUID | `uuid.UUID` |
| `path` | Any non-empty string including `/` | `str` |

```python
path("articles/<int:year>/", views.year_archive),
path("articles/<int:year>/<int:month>/", views.month_archive),
path("articles/<int:year>/<int:month>/<slug:slug>/", views.article_detail),
path("files/<path:file_path>/", views.serve_file),
path("items/<uuid:item_id>/", views.item_detail),
```

## Custom Path Converter

```python
class FourDigitYearConverter:
    regex = "[0-9]{4}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%04d" % value

from django.urls import register_converter
register_converter(FourDigitYearConverter, "yyyy")

urlpatterns = [
    path("articles/<yyyy:year>/", views.year_archive),
]
```

## Regular Expressions with re_path

```python
from django.urls import re_path

urlpatterns = [
    re_path(r"^articles/(?P<year>[0-9]{4})/$", views.year_archive),
    re_path(r"^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$", views.month_archive),
]
```

## Including URLconfs

```python
from django.urls import include, path

urlpatterns = [
    path("blog/", include("blog.urls")),
    path("api/v1/", include("api.v1.urls")),
    path("api/v2/", include("api.v2.urls")),
]

# Include with namespace
path("polls/", include("polls.urls", namespace="author-polls")),

# Include a list of patterns
extra_patterns = [
    path("reports/", views.report),
    path("charge/", views.charge),
]
path("credit/", include(extra_patterns)),
```

## URL Reversing

### In Python

```python
from django.urls import reverse

url = reverse("articles:detail", kwargs={"pk": 42})
url = reverse("articles:detail", args=[42])
url = reverse("articles:list")

# In views
from django.shortcuts import redirect
return redirect("articles:detail", pk=article.pk)
return redirect(article)  # uses get_absolute_url()
```

### In Templates

```html
<a href="{% url 'articles:detail' pk=article.pk %}">{{ article.title }}</a>
<a href="{% url 'articles:list' %}">All Articles</a>

{# With variable arguments #}
{% url 'articles:detail' pk=article.pk as article_url %}
<a href="{{ article_url }}">{{ article.title }}</a>
```

### In Models

```python
from django.urls import reverse

class Article(models.Model):
    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"pk": self.pk})
```

## URL Namespaces

```python
# app/urls.py
app_name = "articles"  # application namespace

# project/urls.py
path("blog/", include("articles.urls")),                                    # namespace = "articles"
path("author-articles/", include("articles.urls", namespace="author")),     # namespace = "author"

# Usage
reverse("articles:list")   # /blog/
reverse("author:list")     # /author-articles/
```

## Passing Extra Options

```python
path("blog/<int:year>/", views.year_archive, {"foo": "bar"}),
# Django calls: views.year_archive(request, year=2024, foo="bar")
```

## Default View Arguments

```python
# URLconf
urlpatterns = [
    path("blog/", views.page),
    path("blog/page<int:num>/", views.page),
]

# View
def page(request, num=1):
    ...
```
