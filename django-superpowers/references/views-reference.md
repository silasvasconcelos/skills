# Django Views Reference (5.0+)

**Views must be thin.** They orchestrate request handling; business logic lives in services, query logic in managers/querysets.

## Function-Based Views

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    if request.method == "POST":
        return redirect("success-url")
    return render(request, "template.html", {"key": "value"})
```

### Shortcut Functions

| Function | Description |
|----------|-------------|
| `render(request, template, context)` | Render template to HttpResponse |
| `redirect(to, *args, **kwargs)` | Return redirect response |
| `get_object_or_404(Model, **kwargs)` | Get object or raise Http404 |
| `get_list_or_404(Model, **kwargs)` | Get list or raise Http404 |

## Class-Based Views (CBVs)

### Generic Display Views

**Always** use Custom Manager/QuerySet methods in `get_queryset()` for DRY + Performance.

```python
from django.views.generic import ListView, DetailView, TemplateView

class ArticleListView(ListView):
    template_name = "articles/list.html"
    context_object_name = "articles"
    paginate_by = 20

    def get_queryset(self):
        # DRY: use manager method (already includes select_related/prefetch_related)
        return Article.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

class ArticleDetailView(DetailView):
    template_name = "articles/detail.html"
    context_object_name = "article"
    slug_field = "slug"

    def get_queryset(self):
        # Performance: always use optimized queryset
        return Article.objects.get_queryset().with_relations()
```

### Generic Editing Views

**Always** use `LoginRequiredMixin` + ownership check on edit/delete views. **Always** set `fields` explicitly.

```python
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OwnerRequiredMixin

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ["title", "slug", "content", "tags"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(OwnerRequiredMixin, UpdateView):
    model = Article
    fields = ["title", "slug", "content", "tags"]
    owner_field = "author"

class ArticleDeleteView(OwnerRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("articles:list")
    owner_field = "author"
```

### Reusable Owner Mixin (DRY)

```python
# mixins.py — use across all apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class OwnerRequiredMixin(LoginRequiredMixin):
    owner_field = "owner"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if getattr(obj, self.owner_field) != self.request.user:
            raise PermissionDenied
        return obj
```

### FormView

```python
class ContactView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = "/thanks/"

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
```

### TemplateView

```python
class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_articles"] = Article.objects.all()[:5]
        return context
```

### RedirectView

```python
from django.views.generic import RedirectView

class ArticleRedirectView(RedirectView):
    pattern_name = "article-detail"
    permanent = False
```

## CBV Hierarchy and Mixins

| Mixin | Provides |
|-------|----------|
| `ContextMixin` | `get_context_data()`, `extra_context` |
| `TemplateResponseMixin` | `render_to_response()`, `template_name` |
| `SingleObjectMixin` | `get_object()`, `model`, `queryset`, `pk_url_kwarg`, `slug_field` |
| `MultipleObjectMixin` | `get_queryset()`, `paginate_by`, `ordering` |
| `FormMixin` | `get_form()`, `form_valid()`, `form_invalid()`, `success_url` |
| `ModelFormMixin` | `form_valid()` with `self.object` save |
| `LoginRequiredMixin` | Require authentication |
| `PermissionRequiredMixin` | Require specific permissions |
| `UserPassesTestMixin` | Custom test function |

## View Decorators

```python
from django.views.decorators.http import require_http_methods, require_GET, require_POST, require_safe
from django.views.decorators.cache import cache_control, never_cache, cache_page
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.gzip import gzip_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@require_http_methods(["GET", "POST"])
def my_view(request):
    ...

# Decorating CBVs
from django.utils.decorators import method_decorator

@method_decorator(login_required, name="dispatch")
class MyView(View):
    ...

# Or in URLconf
path("secret/", login_required(MyView.as_view()))
```

## Async Views

```python
import asyncio
from django.http import HttpResponse

async def async_view(request):
    await asyncio.sleep(1)
    return HttpResponse("Hello async world")

# Class-based async
class AsyncView(View):
    async def get(self, request):
        data = await self.fetch_data()
        return JsonResponse(data)

    async def fetch_data(self):
        ...
```

## Request Object Key Attributes

| Attribute | Description |
|-----------|-------------|
| `request.method` | HTTP method ("GET", "POST", etc.) |
| `request.GET` | QueryDict of GET parameters |
| `request.POST` | QueryDict of POST data |
| `request.FILES` | Dict of uploaded files |
| `request.body` | Raw request body bytes |
| `request.path` | URL path (e.g., "/articles/2024/") |
| `request.user` | Current user (via auth middleware) |
| `request.session` | Session dict |
| `request.META` | Dict of HTTP headers and env vars |
| `request.COOKIES` | Dict of cookies |
| `request.content_type` | MIME type of request body |
| `request.headers` | Case-insensitive dict of HTTP headers |

## Response Classes

| Class | Status Code | Use Case |
|-------|-------------|----------|
| `HttpResponse` | 200 | Generic response |
| `JsonResponse` | 200 | JSON response |
| `HttpResponseRedirect` | 302 | Redirect |
| `HttpResponsePermanentRedirect` | 301 | Permanent redirect |
| `HttpResponseNotFound` | 404 | Not found |
| `HttpResponseForbidden` | 403 | Forbidden |
| `HttpResponseBadRequest` | 400 | Bad request |
| `HttpResponseServerError` | 500 | Server error |
| `HttpResponseNotAllowed` | 405 | Method not allowed |
| `StreamingHttpResponse` | 200 | Streaming content |
| `FileResponse` | 200 | File download |

```python
from django.http import JsonResponse, FileResponse

def api_view(request):
    return JsonResponse({"status": "ok", "data": [1, 2, 3]})

def download_view(request):
    return FileResponse(open("report.pdf", "rb"), as_attachment=True, filename="report.pdf")
```

## File Uploads

```python
def upload_view(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return redirect("success")
    else:
        form = UploadForm()
    return render(request, "upload.html", {"form": form})

def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as dest:
        for chunk in f.chunks():
            dest.write(chunk)
```

## Error Handling

```python
# In root urls.py
handler400 = "myapp.views.bad_request"
handler403 = "myapp.views.permission_denied"
handler404 = "myapp.views.page_not_found"
handler500 = "myapp.views.server_error"
```

## View Performance Rules

1. **Never query the database in templates.** Prepare all data in `get_queryset()` or `get_context_data()`.
2. **Always override `get_queryset()`** in CBVs to use optimized manager methods.
3. **Use `paginate_by`** on all list views — never return unbounded querysets.
4. **Use `cache_page`** for public read-only views with infrequent changes.
5. **Use `only()` / `values()`** in list views when full model data isn't needed.

## View Security Rules

1. **Always** use `LoginRequiredMixin` / `@login_required` on authenticated views.
2. **Always** check object ownership before edit/delete (use `OwnerRequiredMixin`).
3. **Always** use `PermissionRequiredMixin` for role-based access.
4. **Never** trust `request.GET` / `request.POST` without validation.
5. **Use `get_object_or_404()`** to avoid leaking existence information through error types.
6. **Use `require_http_methods`** to restrict allowed HTTP methods on FBVs.
