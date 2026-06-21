# Django Models Reference (5.0+)

## Field Types

### Common Fields

| Field | Description | Key Arguments |
|-------|-------------|---------------|
| `CharField` | Short text | `max_length` (required) |
| `TextField` | Long text | - |
| `IntegerField` | Integer | - |
| `BigIntegerField` | Large integer | - |
| `PositiveIntegerField` | Positive integer | - |
| `FloatField` | Floating point | - |
| `DecimalField` | Fixed precision | `max_digits`, `decimal_places` |
| `BooleanField` | True/False | - |
| `DateField` | Date | `auto_now`, `auto_now_add` |
| `DateTimeField` | Date and time | `auto_now`, `auto_now_add` |
| `TimeField` | Time | - |
| `DurationField` | Time duration | - |
| `EmailField` | Email (validates) | `max_length=254` |
| `URLField` | URL (validates) | `max_length=200` |
| `SlugField` | Slug | `max_length=50`, `allow_unicode` |
| `UUIDField` | UUID | - |
| `FileField` | File upload | `upload_to` |
| `ImageField` | Image upload | `upload_to`, `height_field`, `width_field` |
| `JSONField` | JSON data | `encoder`, `decoder` |
| `BinaryField` | Raw binary | - |
| `GenericIPAddressField` | IP address | `protocol`, `unpack_ipv4` |

### GeneratedField [5.0+]

Database-generated columns whose values are always computed from other fields. Cannot be set manually.

```python
from django.db.models import F, Value
from django.db.models.functions import Concat, Lower

class Product(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.GeneratedField(
        expression=Concat("first_name", Value(" "), "last_name"),
        output_field=models.CharField(max_length=201),
        db_persist=True,
    )

class Rectangle(models.Model):
    length = models.IntegerField()
    width = models.IntegerField()
    area = models.GeneratedField(
        expression=F("length") * F("width"),
        output_field=models.IntegerField(),
        db_persist=True,
    )
```

| Argument | Description |
|---|---|
| `expression` | The database expression used to compute the value |
| `output_field` | The field type of the generated column |
| `db_persist` | `True` = stored column; `False` = virtual column (database-dependent) |

### CompositePrimaryKey [5.2+]

Multi-column primary keys for complex database schemas.

```python
from django.db import models

class Release(models.Model):
    pk = models.CompositePrimaryKey("version", "name")
    version = models.IntegerField()
    name = models.CharField(max_length=20)

class TenantUser(models.Model):
    pk = models.CompositePrimaryKey("tenant_id", "user_id")
    tenant_id = models.IntegerField()
    user_id = models.IntegerField()
```

Access individual primary key fields programmatically via `_meta.pk_fields`.

### Relationship Fields

| Field | Description | Key Arguments |
|-------|-------------|---------------|
| `ForeignKey` | Many-to-one | `to`, `on_delete` (required) |
| `ManyToManyField` | Many-to-many | `to`, `through`, `through_fields` |
| `OneToOneField` | One-to-one | `to`, `on_delete` (required) |

### on_delete Options

| Option | Behavior |
|--------|----------|
| `CASCADE` | Delete related objects |
| `PROTECT` | Prevent deletion |
| `RESTRICT` | Like PROTECT but allows deletion if other cascades handle it |
| `SET_NULL` | Set to NULL (requires `null=True`) |
| `SET_DEFAULT` | Set to default value |
| `SET(value)` | Set to specific value or callable |
| `DO_NOTHING` | Take no action (may break referential integrity) |

## Common Field Options

| Option | Default | Description |
|--------|---------|-------------|
| `null` | `False` | Store empty as NULL |
| `blank` | `False` | Allow empty in forms |
| `choices` | `None` | Limit field to choices |
| `default` | - | Default value or callable |
| `db_default` | - | Database-computed default **[5.0+]** |
| `db_index` | `False` | Create database index |
| `help_text` | `""` | Help text for forms |
| `primary_key` | `False` | Use as primary key |
| `unique` | `False` | Enforce uniqueness |
| `verbose_name` | - | Human-readable name |
| `validators` | `[]` | List of validators |
| `editable` | `True` | Show in forms |
| `error_messages` | - | Custom error messages dict |
| `db_column` | - | Custom database column name |

## Choices with Enumerations

```python
class Status(models.TextChoices):
    DRAFT = "DR", "Draft"
    PUBLISHED = "PB", "Published"
    ARCHIVED = "AR", "Archived"

class Article(models.Model):
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)

# Usage
article.status  # "DR"
article.get_status_display()  # "Draft"
article.status == Status.DRAFT  # True

class Priority(models.IntegerChoices):
    LOW = 1, "Low"
    MEDIUM = 2, "Medium"
    HIGH = 3, "High"
```

### Simplified Choices [5.0+]

In addition to enums and 2-tuples, choices can now be a mapping or a flat iterable:

```python
# Mapping (dict) — keys are stored, values are display labels
status = models.CharField(max_length=10, choices={"draft": "Draft", "published": "Published"})

# Flat iterable — value used as both stored value and display label
color = models.CharField(max_length=10, choices=["red", "green", "blue"])
```

## Meta Options

```python
class Article(models.Model):
    class Meta:
        ordering = ["-pub_date", "title"]
        verbose_name = "article"
        verbose_name_plural = "articles"
        db_table = "custom_table_name"
        unique_together = [["author", "title"]]  # deprecated, use constraints
        indexes = [
            models.Index(fields=["pub_date"]),
            models.Index(fields=["title", "pub_date"], name="title_date_idx"),
        ]
        constraints = [
            models.UniqueConstraint(fields=["author", "title"], name="unique_author_title"),
            models.CheckConstraint(check=models.Q(rating__gte=1), name="rating_gte_1"),
        ]
        abstract = False
        proxy = False
        managed = True
        default_related_name = "%(model_name)ss"
        get_latest_by = "pub_date"
        permissions = [("can_publish", "Can publish articles")]
```

## Model Inheritance

### Abstract Base Class (no table)

```python
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Article(TimeStampedModel):
    title = models.CharField(max_length=200)
```

### Multi-table Inheritance (separate tables, implicit OneToOneField)

```python
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_pizza = models.BooleanField(default=False)
```

### Proxy Model (same table, different Python behavior)

```python
class OrderedArticle(Article):
    class Meta:
        proxy = True
        ordering = ["title"]
```

## QuerySet API

### Creating

```python
obj = Model.objects.create(**kwargs)
obj = Model(**kwargs); obj.save()
objs = Model.objects.bulk_create([Model(**kw1), Model(**kw2)])
obj, created = Model.objects.get_or_create(defaults={...}, **lookup)
obj, created = Model.objects.update_or_create(defaults={...}, **lookup)
```

### Retrieving

```python
qs = Model.objects.all()
qs = Model.objects.filter(**kwargs)
qs = Model.objects.exclude(**kwargs)
obj = Model.objects.get(**kwargs)
obj = Model.objects.first()
obj = Model.objects.last()
exists = Model.objects.filter(**kwargs).exists()
count = Model.objects.count()
```

### Filtering (Field Lookups)

```python
field__exact=value        # == (default)
field__iexact=value       # case-insensitive ==
field__contains=value     # LIKE '%value%'
field__icontains=value    # case-insensitive contains
field__startswith=value   # LIKE 'value%'
field__endswith=value     # LIKE '%value'
field__in=[1, 2, 3]      # IN clause
field__gt=value           # >
field__gte=value          # >=
field__lt=value           # <
field__lte=value          # <=
field__range=(start, end) # BETWEEN
field__isnull=True        # IS NULL
field__year=2024          # date year
field__month=1            # date month
field__day=15             # date day
field__regex=r'^pattern'  # regex match
```

### Spanning Relationships

```python
Entry.objects.filter(blog__name="Beatles Blog")
Blog.objects.filter(entry__headline__contains="Lennon")
Entry.objects.filter(blog__id=3)  # or blog__pk=3
```

### Ordering, Slicing, Aggregation

```python
qs = Model.objects.order_by("-pub_date", "title")
qs = Model.objects.all()[:5]      # LIMIT 5
qs = Model.objects.all()[5:10]    # OFFSET 5 LIMIT 5

from django.db.models import Avg, Count, Max, Min, Sum
Model.objects.aggregate(avg_price=Avg("price"))
Model.objects.annotate(num_entries=Count("entry"))
```

### Updating and Deleting

```python
Model.objects.filter(**kwargs).update(field=value)
Model.objects.filter(**kwargs).delete()
obj.delete()
```

### Performance Optimization

**All queries MUST be optimized. Never allow N+1 queries.**

```python
# select_related: FK/O2O — generates a JOIN (one query)
qs = Article.objects.select_related("author", "category")

# prefetch_related: M2M/reverse FK — generates separate query + Python join
qs = Article.objects.prefetch_related("tags", "comments")

# Combine both for complex traversals
qs = Article.objects.select_related("author").prefetch_related("tags")

# only/defer: load specific fields (avoids loading large text/binary columns)
qs = Article.objects.only("title", "created_at")
qs = Article.objects.defer("content")

# values/values_list: dict/tuple results (no model instantiation overhead)
qs = Article.objects.values("title", "author__name")
qs = Article.objects.values_list("title", flat=True)

# exists(): more efficient than count() > 0
if Article.objects.filter(author=user).exists():
    ...

# iterator(): for large querysets, avoids caching all results in memory
for article in Article.objects.iterator(chunk_size=2000):
    process(article)

# bulk operations: avoid N queries from loop-based .save()
Article.objects.bulk_create([Article(...), Article(...)])
Article.objects.bulk_update(articles, fields=["status"])
Article.objects.filter(status="draft").update(status="archived")
Article.objects.filter(status="archived").delete()
```

### Subqueries and Annotations

```python
from django.db.models import Subquery, OuterRef, Exists, Count, Avg

# Subquery: get latest comment date per article
latest_comment = Comment.objects.filter(
    article=OuterRef("pk"),
).order_by("-created_at").values("created_at")[:1]

articles = Article.objects.annotate(
    latest_comment_date=Subquery(latest_comment),
)

# Exists: efficient boolean check
has_comments = Comment.objects.filter(article=OuterRef("pk"))
articles = Article.objects.annotate(has_comments=Exists(has_comments))

# Aggregation with annotation
articles = Article.objects.annotate(
    comment_count=Count("comments"),
    avg_rating=Avg("ratings__score"),
).order_by("-comment_count")
```

### Database Indexes

```python
class Article(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["author", "status"]),
            models.Index(
                fields=["title"],
                condition=Q(status="published"),
                name="published_title_idx",
            ),
        ]
```

### F and Q Expressions

```python
from django.db.models import F, Q

Entry.objects.filter(number_of_comments__gt=F("number_of_pingbacks"))
Entry.objects.filter(rating__lt=F("number_of_comments") + F("number_of_pingbacks"))
Entry.objects.update(number_of_pingbacks=F("number_of_pingbacks") + 1)

Entry.objects.filter(Q(headline__startswith="What") | Q(headline__startswith="Who"))
Entry.objects.filter(Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)))
Entry.objects.exclude(~Q(pub_date__year=2005))
```

## Overriding Model Methods

```python
class Blog(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        if (update_fields := kwargs.get("update_fields")) is not None and "name" in update_fields:
            kwargs["update_fields"] = {"slug"}.union(update_fields)
        super().save(**kwargs)
```

## Custom QuerySets and Managers (DRY Pattern)

**Every model MUST have** a Custom QuerySet and a Custom Manager. They are the primary DRY mechanism for queries. QuerySets, Managers, and Models MUST be organized as packages at the app level — one class per module, re-exported from `__init__.py`.

### App-Level Package Structure

```
myapp/
├── querysets/
│   ├── __init__.py               # re-exports ArticleQuerySet
│   └── article_query_set.py      # ArticleQuerySet class
├── managers/
│   ├── __init__.py               # re-exports ArticleManager
│   └── article_manager.py        # ArticleManager class
├── models/
│   ├── __init__.py               # re-exports Article
│   └── article.py                # Article model
├── migrations/
├── admin.py
├── apps.py
├── tests.py
└── views.py
```

### Custom QuerySet — `myapp/querysets/article_query_set.py`

```python
from django.db import models
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta


class ArticleQuerySet(models.QuerySet):
    """Reusable, chainable query filters."""

    def published(self):
        from myapp.models import Article

        return self.filter(status=Article.Status.PUBLISHED)

    def draft(self):
        from myapp.models import Article

        return self.filter(status=Article.Status.DRAFT)

    def by_author(self, user):
        return self.filter(author=user)

    def recent(self, days=30):
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=cutoff)

    def with_relations(self):
        """Always call this when rendering articles with author/tags."""
        return self.select_related("author").prefetch_related("tags")

    def with_comment_count(self):
        return self.annotate(comment_count=Count("comments"))

    def search(self, query):
        return self.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
```

### Re-export — `myapp/querysets/__init__.py`

```python
from myapp.querysets.article_query_set import ArticleQuerySet

__all__ = ["ArticleQuerySet"]
```

### Custom Manager — `myapp/managers/article_manager.py`

```python
from django.db import models

from myapp.querysets import ArticleQuerySet


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published().with_relations()

    def recent_published(self, days=30):
        return self.get_queryset().published().recent(days).with_relations()
```

### Re-export — `myapp/managers/__init__.py`

```python
from myapp.managers.article_manager import ArticleManager

__all__ = ["ArticleManager"]
```

### Model — `myapp/models/article.py`

```python
from django.db import models

from myapp.managers import ArticleManager


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    # ... fields ...

    objects = ArticleManager()
```

### Re-export — `myapp/models/__init__.py`

```python
from myapp.models.article import Article

__all__ = ["Article"]
```

### Using in views (DRY)

```python
# Instead of repeating filters in every view:
# BAD:
Article.objects.filter(status="published").select_related("author")

# GOOD:
Article.objects.published()  # Manager method already includes with_relations()

# Chaining QuerySet methods:
Article.objects.published().by_author(user).recent(7)
```

### Multiple Managers

```python
# myapp/models/article.py
class Article(models.Model):
    objects = ArticleManager()  # default (full access)
    published = PublishedOnlyManager()  # filtered default queryset

    class Meta:
        default_manager_name = "objects"
```

## Abstract Base Models (DRY Pattern)

**Always** create abstract base models for fields shared across multiple models. Abstract models, their QuerySets, and Managers follow the same package structure.

### `myapp/querysets/soft_delete_query_set.py`

```python
from django.db import models


class SoftDeleteQuerySet(models.QuerySet):
    def active(self):
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)
```

### `myapp/managers/soft_delete_manager.py`

```python
from django.db import models

from myapp.querysets import SoftDeleteQuerySet


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).active()
```

### `myapp/models/timestamped.py`

```python
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
```

### `myapp/models/soft_delete.py`

```python
from django.db import models
from django.utils import timezone

from myapp.managers import SoftDeleteManager


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])
```

### `myapp/models/owned.py`

```python
from django.conf import settings
from django.db import models


class OwnedModel(models.Model):
    """Mixin for models owned by a user."""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
    )

    class Meta:
        abstract = True
```

### Composing abstract base models

```python
# myapp/models/article.py
class Article(TimeStampedModel, SoftDeleteModel, OwnedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
```

## Many-to-Many with Through Model

```python
class Person(models.Model):
    name = models.CharField(max_length=128)

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through="Membership")

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    role = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["person", "group"], name="unique_membership")
        ]
```
