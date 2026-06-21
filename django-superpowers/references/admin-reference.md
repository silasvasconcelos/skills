# Django Admin Reference (5.0+)

## Basic Registration

```python
from django.contrib import admin
from .models import Article

# Simple registration
admin.site.register(Article)

# Decorator-based (recommended)
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass
```

## ModelAdmin Options

### List View

```python
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "pub_date", "status", "is_published"]
    list_display_links = ["title"]           # clickable fields
    list_filter = ["status", "pub_date", "author"]
    list_editable = ["status"]               # inline editing
    list_per_page = 25                       # pagination
    list_max_show_all = 200
    list_select_related = ["author"]         # optimize queries
    search_fields = ["title", "content", "author__username"]
    search_help_text = "Search by title, content, or author"
    ordering = ["-pub_date"]
    date_hierarchy = "pub_date"
    sortable_by = ["title", "pub_date"]
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = False
    show_facets = admin.ShowFacets.ALWAYS    # show filter counts [5.0+]
```

### Detail/Form View

```python
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ["title", "slug", "content", ("author", "status"), "pub_date", "tags"]
    readonly_fields = ["created_at", "updated_at"]
    exclude = ["secret_field"]
    fieldsets = [
        (None, {
            "fields": ["title", "slug", "content"],
        }),
        ("Publishing", {
            "fields": ["author", "status", "pub_date"],
            "classes": ["collapse"],
        }),
        ("Metadata", {
            "fields": ["tags", "created_at", "updated_at"],
            "classes": ["wide"],
        }),
    ]
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["author"]
    raw_id_fields = ["author"]
    filter_horizontal = ["tags"]              # for M2M
    filter_vertical = ["categories"]          # for M2M (vertical)
    save_on_top = True
    save_as = False
    save_as_continue = True
    view_on_site = True
```

### Custom Display Methods

```python
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author_name", "is_published", "colored_status"]

    @admin.display(description="Author", ordering="author__last_name")
    def author_name(self, obj):
        return obj.author.get_full_name()

    @admin.display(boolean=True, description="Published?")
    def is_published(self, obj):
        return obj.status == "published"

    @admin.display(description="Status")
    def colored_status(self, obj):
        from django.utils.html import format_html
        colors = {"draft": "gray", "published": "green", "archived": "red"}
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, "black"),
            obj.get_status_display(),
        )
```

## Inline Models

```python
class CommentInline(admin.TabularInline):   # or admin.StackedInline
    model = Comment
    extra = 1                                # number of empty forms
    min_num = 0
    max_num = 10
    show_change_link = True
    readonly_fields = ["created_at"]
    autocomplete_fields = ["author"]

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
```

## Admin Actions

```python
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    actions = ["make_published", "make_draft"]

    @admin.action(description="Mark selected as published")
    def make_published(self, request, queryset):
        updated = queryset.update(status="published")
        self.message_user(request, f"{updated} articles published.")

    @admin.action(description="Mark selected as draft")
    def make_draft(self, request, queryset):
        queryset.update(status="draft")
```

## Overriding Methods

```python
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:  # creating new
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(author=request.user)
        return qs

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing existing
            return ["slug", "author"]
        return []

    def has_change_permission(self, request, obj=None):
        if obj and obj.author != request.user and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields["status"].disabled = True
        return form
```

## Admin Site Customization

```python
# admin.py or apps.py
admin.site.site_header = "My Project Admin"
admin.site.site_title = "My Project"
admin.site.index_title = "Dashboard"
admin.site.site_url = "/"
admin.site.enable_nav_sidebar = True
```

## Custom Admin Site

```python
class MyAdminSite(admin.AdminSite):
    site_header = "Custom Admin"
    site_title = "Custom Admin Portal"

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        # customize ordering
        return app_list

my_admin = MyAdminSite(name="myadmin")
my_admin.register(Article, ArticleAdmin)

# urls.py
path("myadmin/", my_admin.urls),
```
