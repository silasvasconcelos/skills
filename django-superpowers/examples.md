# Django Common Patterns & Examples (5.0+)

All examples follow the four core principles: **Performance**, **Security**, **DRY**, and **Best Practices**.

## 1. Complete CRUD App Pattern (with DRY + Performance + Security)

### Base Models (DRY)

```python
# core/models.py
from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
```

### Model with Custom QuerySet + Manager

```python
# articles/models.py
from django.db import models
from django.db.models import Count, Q
from django.urls import reverse
from core.models import TimeStampedModel


class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=Article.Status.PUBLISHED)

    def draft(self):
        return self.filter(status=Article.Status.DRAFT)

    def by_author(self, user):
        return self.filter(author=user)

    def with_relations(self):
        return self.select_related("author").prefetch_related("tags")

    def with_stats(self):
        return self.annotate(comment_count=Count("comments"))

    def search(self, query):
        return self.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published().with_relations()


class Article(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="articles",
    )
    status = models.CharField(max_length=10, choices=Status, default=Status.DRAFT)
    tags = models.ManyToManyField("Tag", blank=True, related_name="articles")

    objects = ArticleManager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["author", "status"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_author_title",
            ),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"slug": self.slug})
```

### Service Layer (DRY + Security + Performance)

```python
# articles/services.py
from django.core.exceptions import PermissionDenied
from django.db import transaction
from .models import Article


class ArticleService:
    @staticmethod
    @transaction.atomic
    def create_article(user, data):
        article = Article(author=user, **data)
        article.full_clean()
        article.save()
        return article

    @staticmethod
    @transaction.atomic
    def update_article(article_id, user, data):
        article = Article.objects.select_for_update().get(pk=article_id)
        if article.author != user:
            raise PermissionDenied("You do not own this article.")
        for field, value in data.items():
            setattr(article, field, value)
        article.full_clean()
        article.save(update_fields=list(data.keys()) + ["updated_at"])
        return article

    @staticmethod
    @transaction.atomic
    def publish_article(article_id, user):
        article = Article.objects.select_for_update().get(pk=article_id)
        if article.author != user and not user.has_perm("articles.can_publish"):
            raise PermissionDenied("You cannot publish this article.")
        article.status = Article.Status.PUBLISHED
        article.save(update_fields=["status", "updated_at"])
        return article

    @staticmethod
    @transaction.atomic
    def delete_article(article_id, user):
        article = Article.objects.select_for_update().get(pk=article_id)
        if article.author != user:
            raise PermissionDenied("You do not own this article.")
        article.delete()
```

### Views (thin, using service + manager)

```python
# articles/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Article
from .mixins import OwnerRequiredMixin


class ArticleListView(ListView):
    paginate_by = 10
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.published()


class ArticleDetailView(DetailView):
    context_object_name = "article"

    def get_queryset(self):
        return Article.objects.get_queryset().with_relations()


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ["title", "slug", "content", "status", "tags"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(OwnerRequiredMixin, UpdateView):
    model = Article
    fields = ["title", "slug", "content", "status", "tags"]
    owner_field = "author"


class ArticleDeleteView(OwnerRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("articles:list")
    owner_field = "author"
```

### Owner Mixin (DRY - reusable across apps)

```python
# articles/mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class OwnerRequiredMixin(LoginRequiredMixin):
    """Reusable mixin: ensures the current user owns the object."""
    owner_field = "owner"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if getattr(obj, self.owner_field) != self.request.user:
            raise PermissionDenied
        return obj
```

### URLs

```python
# articles/urls.py
from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="list"),
    path("create/", views.ArticleCreateView.as_view(), name="create"),
    path("<slug:slug>/", views.ArticleDetailView.as_view(), name="detail"),
    path("<slug:slug>/edit/", views.ArticleUpdateView.as_view(), name="edit"),
    path("<slug:slug>/delete/", views.ArticleDeleteView.as_view(), name="delete"),
]
```

### Admin

```python
# articles/admin.py
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
```

## 2. REST API Pattern (with DRF - Performance + Security)

```python
# api/serializers.py
from rest_framework import serializers
from articles.models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views (only needed fields)."""
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Article
        fields = ["id", "title", "slug", "author", "status", "created_at"]
        read_only_fields = ["author", "created_at"]


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail/create/update."""
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Article
        fields = ["id", "title", "slug", "content", "author", "status", "tags", "created_at"]
        read_only_fields = ["author", "created_at"]


# api/views.py
from rest_framework import viewsets, permissions
from articles.models import Article
from .serializers import ArticleListSerializer, ArticleDetailSerializer
from .permissions import IsOwnerOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        # Performance: use manager method with select/prefetch
        return Article.objects.published()

    def get_serializer_class(self):
        # DRY: separate serializers for list vs detail
        if self.action == "list":
            return ArticleListSerializer
        return ArticleDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# api/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """Reusable permission: only the owner can mutate."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

router = DefaultRouter()
router.register(r"articles", ArticleViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
```

## 3. Custom User Model Pattern

```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    def __str__(self):
        return self.email

# settings.py
AUTH_USER_MODEL = "accounts.CustomUser"
```

## 4. Signal Pattern

```python
# articles/signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Article

@receiver(post_save, sender=Article)
def article_saved(sender, instance, created, **kwargs):
    if created:
        notify_subscribers(instance)

@receiver(pre_delete, sender=Article)
def article_deleted(sender, instance, **kwargs):
    cleanup_related_data(instance)

# articles/apps.py
class ArticlesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "articles"

    def ready(self):
        import articles.signals  # noqa: F401
```

## 5. Service Layer Pattern (DRY + Security + Performance)

**Always** put business logic in a service layer. Views should only orchestrate.

```python
# articles/services.py
from functools import partial
from django.core.exceptions import PermissionDenied
from django.db import transaction
from .models import Article
from .tasks import send_publish_notification


class ArticleService:
    @staticmethod
    @transaction.atomic
    def publish_article(article_id, user):
        article = Article.objects.select_for_update().get(pk=article_id)
        if article.author != user and not user.has_perm("articles.can_publish"):
            raise PermissionDenied("You cannot publish this article.")
        article.status = Article.Status.PUBLISHED
        article.save(update_fields=["status", "updated_at"])
        transaction.on_commit(
            partial(send_publish_notification.enqueue, article_id=article.id)
        )
        return article

    @staticmethod
    @transaction.atomic
    def bulk_archive(author, days_old=90):
        """Archive old draft articles for a given author."""
        from django.utils import timezone
        from datetime import timedelta

        cutoff = timezone.now() - timedelta(days=days_old)
        return Article.objects.filter(
            author=author,
            status=Article.Status.DRAFT,
            created_at__lt=cutoff,
        ).update(status="archived")


# articles/views.py
class PublishArticleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        article = ArticleService.publish_article(pk, request.user)
        messages.success(request, f"'{article.title}' published.")
        return redirect(article)
```

### When to use the Service Layer

| Logic Type | Where |
|---|---|
| Simple CRUD (create/update via form) | View + ModelForm |
| Business rules, permission checks, multi-model ops | Service Layer |
| Reusable query filters | Custom QuerySet/Manager |
| Computed properties | Model methods/properties |
| Side effects (email, tasks) | Service Layer + `on_commit` |

## 6. Background Task Pattern [6.0+]

```python
# articles/tasks.py
from django.tasks import task
from django.core.mail import send_mass_mail

@task
def send_publish_notification(article_id):
    from .models import Article
    article = Article.objects.select_related("author").get(pk=article_id)
    subscribers = article.author.subscribers.values_list("email", flat=True)
    messages = [
        (
            f"New article: {article.title}",
            f"{article.author} published a new article.",
            None,
            [email],
        )
        for email in subscribers
    ]
    return send_mass_mail(messages)

@task(priority=5)
def generate_thumbnail(image_id):
    from .models import Image
    image = Image.objects.get(pk=image_id)
    create_thumbnail(image.file.path)
    image.thumbnail_generated = True
    image.save(update_fields=["thumbnail_generated"])

# Usage in views
from functools import partial
from django.db import transaction

def upload_image(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                image = form.save()
                transaction.on_commit(partial(
                    generate_thumbnail.enqueue, image_id=image.id
                ))
            return redirect("images:detail", pk=image.pk)
    ...
```

## 7. Async View Pattern

```python
import asyncio
import httpx
from django.http import JsonResponse

async def aggregated_api_view(request):
    async with httpx.AsyncClient() as client:
        weather, news, stocks = await asyncio.gather(
            client.get("https://api.weather.com/current"),
            client.get("https://api.news.com/top"),
            client.get("https://api.stocks.com/market"),
        )
    return JsonResponse({
        "weather": weather.json(),
        "news": news.json(),
        "stocks": stocks.json(),
    })
```

## 8. Multi-Database Pattern

```python
# settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "primary_db",
    },
    "replica": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "replica_db",
    },
}

DATABASE_ROUTERS = ["myapp.routers.PrimaryReplicaRouter"]

# myapp/routers.py
class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        return "replica"

    def db_for_write(self, model, **hints):
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default"
```

## 9. Caching Pattern

```python
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# View-level caching
@cache_page(60 * 15)  # 15 minutes
def my_view(request):
    ...

# Low-level caching
def get_articles():
    articles = cache.get("published_articles")
    if articles is None:
        articles = list(Article.objects.filter(status="published"))
        cache.set("published_articles", articles, timeout=300)
    return articles

# Template fragment caching
# {% load cache %}
# {% cache 500 sidebar request.user.id %}
#     ... expensive template fragment ...
# {% endcache %}

# Cache invalidation
def save_article(article):
    article.save()
    cache.delete("published_articles")
    cache.delete(f"article_{article.pk}")
```

## 10. Management Command Pattern (with Performance)

```python
# myapp/management/commands/import_data.py
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from myapp.models import Article


class Command(BaseCommand):
    help = "Import articles from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to CSV file")
        parser.add_argument("--dry-run", action="store_true", help="Simulate without saving")
        parser.add_argument("--batch-size", type=int, default=1000)

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        dry_run = options["dry_run"]
        batch_size = options["batch_size"]

        try:
            count = self.import_articles(csv_file, dry_run, batch_size)
        except FileNotFoundError:
            raise CommandError(f"File not found: {csv_file}")

        if dry_run:
            self.stdout.write(self.style.WARNING(f"Dry run: would import {count} articles"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Imported {count} articles"))

    @transaction.atomic
    def import_articles(self, csv_file, dry_run, batch_size):
        import csv

        with open(csv_file) as f:
            reader = csv.DictReader(f)
            articles = [Article(**row) for row in reader]

        if not dry_run:
            Article.objects.bulk_create(articles, batch_size=batch_size)

        return len(articles)
```

## 11. Query Performance Anti-Patterns

```python
# BAD: N+1 query — one query per article to get author
articles = Article.objects.all()
for article in articles:
    print(article.author.name)  # hits DB for each article!

# GOOD: one query with JOIN
articles = Article.objects.select_related("author")
for article in articles:
    print(article.author.name)  # no extra query

# BAD: loading all fields for a list view
articles = Article.objects.all()  # loads content, which can be huge

# GOOD: load only needed fields
articles = Article.objects.only("title", "slug", "created_at")
# or use values for even less overhead
articles = Article.objects.values("title", "slug", "created_at")

# BAD: checking existence by counting
if Article.objects.filter(author=user).count() > 0:  # counts ALL rows
    ...

# GOOD: use exists() — stops at first match
if Article.objects.filter(author=user).exists():
    ...

# BAD: updating in a loop
for article in Article.objects.filter(status="draft"):
    article.status = "archived"
    article.save()  # N queries!

# GOOD: single UPDATE query
Article.objects.filter(status="draft").update(status="archived")

# BAD: incrementing a counter in Python (race condition)
article = Article.objects.get(pk=1)
article.view_count += 1  # another request could read stale value
article.save()

# GOOD: atomic increment with F()
from django.db.models import F
Article.objects.filter(pk=1).update(view_count=F("view_count") + 1)
```

## 12. Testing with Query Assertions

```python
from django.test import TestCase


class ArticleQueryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("testuser", password="pass")
        for i in range(10):
            Article.objects.create(
                title=f"Article {i}",
                content="content",
                author=cls.user,
                status=Article.Status.PUBLISHED,
            )

    def test_list_view_query_count(self):
        """Ensure listing articles uses a fixed number of queries."""
        with self.assertNumQueries(2):  # 1 for articles+author, 1 for tags
            list(Article.objects.published())

    def test_service_publish_uses_select_for_update(self):
        article = Article.objects.first()
        with self.assertNumQueries(3):  # SELECT FOR UPDATE, UPDATE, on_commit
            ArticleService.publish_article(article.pk, self.user)
```
