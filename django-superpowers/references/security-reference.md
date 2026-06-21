# Django Security Reference (5.0+)

**Security is non-negotiable.** Every view, form, serializer, and service must be written with security in mind.

## Mandatory Security Checklist

Apply this checklist to every feature:

- [ ] All user input is validated (forms, serializers, query params)
- [ ] `fields` is explicitly set on ModelForm/Serializer (never `__all__`)
- [ ] Object-level permissions checked before any mutation (ownership, roles)
- [ ] `LoginRequiredMixin` / `@login_required` on all authenticated views
- [ ] `{% csrf_token %}` in every POST form
- [ ] No `raw()` / `extra()` / `RawSQL` with string interpolation
- [ ] No `|safe` / `mark_safe()` on unsanitized user input
- [ ] `select_for_update()` on critical write paths to prevent race conditions
- [ ] Sensitive operations wrapped in `transaction.atomic()`
- [ ] File uploads validated (type, size, extension)
- [ ] Rate limiting on authentication and sensitive endpoints
- [ ] `manage.py check --deploy` passes before deployment

## Built-in Protections

### Cross-Site Scripting (XSS)

- Django templates auto-escape HTML by default.
- Dangerous: `mark_safe()`, `|safe` filter, `{% autoescape off %}`.
- Never insert user data into `<script>`, `<style>`, or HTML attributes without escaping.

```python
# Safe - auto-escaped
{{ user_input }}

# Dangerous - bypasses escaping
{{ user_input|safe }}
{% autoescape off %}{{ user_input }}{% endautoescape %}

# If you must mark as safe, sanitize first
from django.utils.html import escape, format_html
safe_html = format_html("<b>{}</b>", user_input)  # escapes user_input
```

### Cross-Site Request Forgery (CSRF)

- `CsrfViewMiddleware` enabled by default.
- All POST forms must include `{% csrf_token %}`.
- For AJAX, include CSRF token in headers.

```html
<form method="post">
    {% csrf_token %}
    {{ form }}
    <button type="submit">Submit</button>
</form>
```

```javascript
// AJAX with CSRF
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
});
```

```python
# Exempt a view from CSRF (use sparingly)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def webhook_view(request):
    ...
```

### SQL Injection

- ORM querysets use parameterized queries (safe by default).
- Be careful with `raw()`, `extra()`, `RawSQL`.

```python
# Safe - parameterized
Model.objects.filter(name=user_input)
Model.objects.raw("SELECT * FROM app_model WHERE name = %s", [user_input])

# DANGEROUS - string interpolation
Model.objects.raw(f"SELECT * FROM app_model WHERE name = '{user_input}'")
```

### Clickjacking

- `XFrameOptionsMiddleware` sets `X-Frame-Options: DENY` by default.

```python
# Settings
X_FRAME_OPTIONS = "DENY"          # default
X_FRAME_OPTIONS = "SAMEORIGIN"    # allow same-origin framing

# Per-view override
from django.views.decorators.clickjacking import xframe_options_deny, xframe_options_sameorigin, xframe_options_exempt

@xframe_options_sameorigin
def my_view(request):
    ...
```

### Host Header Validation

```python
ALLOWED_HOSTS = ["example.com", ".example.com"]  # dot prefix matches subdomains
```

## Content Security Policy [6.0+]

CSP controls which resources the browser is allowed to load.

```python
# settings.py
MIDDLEWARE = [
    ...
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csp.ContentSecurityPolicyMiddleware",  # add CSP middleware
    ...
]

# CSP directives
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src": ["'self'", "https://cdn.example.com"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:", "https:"],
        "font-src": ["'self'", "https://fonts.gstatic.com"],
        "connect-src": ["'self'"],
        "frame-ancestors": ["'none'"],
    },
}

# Report-only mode (monitor without enforcing)
CONTENT_SECURITY_POLICY_REPORT_ONLY = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "report-uri": ["/csp-report/"],
    },
}
```

```python
# Per-view CSP override
from django.views.decorators.csp import csp_override

@csp_override({"script-src": ["'self'", "'unsafe-inline'"]})
def my_view(request):
    ...
```

## HTTPS Settings

```python
# Redirect HTTP to HTTPS
SECURE_SSL_REDIRECT = True
SECURE_REDIRECT_EXEMPT = []  # URL patterns exempt from redirect

# Behind a proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000            # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookie security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Other
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
```

## Password Security

```python
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Password hashers (default order)
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]
```

## Cryptographic Signing

```python
from django.core.signing import Signer, TimestampSigner

# Simple signing
signer = Signer()
signed = signer.sign("my-data")
original = signer.unsign(signed)

# Time-limited signing
signer = TimestampSigner()
signed = signer.sign("my-data")
original = signer.unsign(signed, max_age=3600)  # 1 hour
```

## Deployment Checklist

Run `python manage.py check --deploy` to verify:

- `DEBUG = False`
- `SECRET_KEY` is set and unique
- `ALLOWED_HOSTS` is configured
- HTTPS settings are enabled
- CSRF and session cookies are secure
- HSTS is configured
- `X_FRAME_OPTIONS` is set

## User-Uploaded Content Security

- Serve uploads from a separate domain or subdomain.
- Validate file types and sizes.
- Never serve uploads with `X-Content-Type-Options: nosniff` disabled.
- Use `MEDIA_ROOT` outside the source code directory.

```python
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def validate_file_size(value):
    max_size = 10 * 1024 * 1024  # 10MB
    if value.size > max_size:
        raise ValidationError(f"File size must be under {max_size // (1024*1024)}MB.")

class Document(models.Model):
    file = models.FileField(
        upload_to="documents/%Y/%m/",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"]),
            validate_file_size,
        ],
    )
```

## Input Validation Patterns

### Always validate query parameters

```python
from django.core.exceptions import ValidationError

def article_search(request):
    query = request.GET.get("q", "").strip()
    if not query or len(query) > 200:
        return HttpResponseBadRequest("Invalid search query.")
    page = request.GET.get("page", "1")
    if not page.isdigit() or int(page) < 1:
        return HttpResponseBadRequest("Invalid page number.")
    articles = Article.objects.published().search(query)
    ...
```

### Always validate object ownership in services

```python
from django.core.exceptions import PermissionDenied

class ArticleService:
    @staticmethod
    def update_article(article_id, user, data):
        article = Article.objects.select_for_update().get(pk=article_id)
        if article.author != user and not user.has_perm("articles.change_article"):
            raise PermissionDenied("You do not own this article.")
        for field, value in data.items():
            setattr(article, field, value)
        article.full_clean()
        article.save(update_fields=list(data.keys()) + ["updated_at"])
        return article
```

### Prevent mass assignment

```python
# BAD: accepts any field from the request
Article.objects.create(**request.POST.dict())

# GOOD: explicit fields through a validated form/serializer
form = ArticleForm(request.POST)
if form.is_valid():
    article = form.save(commit=False)
    article.author = request.user
    article.save()
```

## Secure Concurrency Patterns

```python
from django.db import transaction
from django.db.models import F

# Use F() for atomic increments (avoids race conditions)
Article.objects.filter(pk=article_id).update(view_count=F("view_count") + 1)

# Use select_for_update for read-modify-write
with transaction.atomic():
    account = Account.objects.select_for_update().get(pk=account_id)
    if account.balance < amount:
        raise ValueError("Insufficient balance.")
    account.balance -= amount
    account.save(update_fields=["balance"])
```

## Rate Limiting

```python
# Using django-ratelimit (third-party) or custom middleware
from django.core.cache import cache
from django.http import HttpResponseTooManyRequests

def rate_limit(key_prefix, limit=10, period=60):
    """Simple rate limiter using cache."""
    def decorator(view_func):
        def wrapped(request, *args, **kwargs):
            key = f"ratelimit:{key_prefix}:{request.META.get('REMOTE_ADDR')}"
            requests_count = cache.get(key, 0)
            if requests_count >= limit:
                return HttpResponseTooManyRequests("Rate limit exceeded.")
            cache.set(key, requests_count + 1, period)
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator
```
