# Django Authentication Reference (5.0+)

## Custom User Model (Recommended)

Set `AUTH_USER_MODEL` before running the first migration.

```python
# settings.py
AUTH_USER_MODEL = "accounts.CustomUser"
```

```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Profile", {"fields": ("bio", "avatar")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Profile", {"fields": ("bio", "avatar")}),
    )
```

### AbstractBaseUser (Full Control)

```python
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email
```

## Authentication Views (Built-in)

```python
# urls.py
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

# Or use the shortcut
path("accounts/", include("django.contrib.auth.urls")),
```

Required templates:
- `registration/login.html`
- `registration/logged_out.html`
- `registration/password_change_form.html`
- `registration/password_change_done.html`
- `registration/password_reset_form.html`
- `registration/password_reset_done.html`
- `registration/password_reset_confirm.html`
- `registration/password_reset_complete.html`
- `registration/password_reset_email.html`

## Global Login Required [5.1+]

Use `LoginRequiredMiddleware` to require authentication for all views by default, then exempt public views with `login_not_required`.

```python
# settings.py
MIDDLEWARE = [
    ...
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.LoginRequiredMiddleware",
    ...
]

# Exempt public views
from django.contrib.auth.decorators import login_not_required

@login_not_required
def public_view(request):
    ...
```

This replaces the need to add `@login_required` or `LoginRequiredMixin` to every authenticated view.

## Authentication in Views

### Function-Based

```python
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate, login, logout

@login_required
def profile_view(request):
    return render(request, "profile.html")

@login_required(login_url="/custom-login/")
def restricted_view(request):
    ...

@permission_required("myapp.can_publish", raise_exception=True)
def publish_view(request):
    ...

@user_passes_test(lambda u: u.is_staff)
def staff_view(request):
    ...

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("home")
```

### Class-Based

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ["title", "content"]
    login_url = "/login/"
    redirect_field_name = "next"

class PublishView(PermissionRequiredMixin, View):
    permission_required = "myapp.can_publish"
    # or multiple: permission_required = ("myapp.can_publish", "myapp.can_edit")

class AuthorOnlyView(UserPassesTestMixin, DetailView):
    model = Article

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author
```

## User Model API

```python
from django.contrib.auth import get_user_model

User = get_user_model()

# Create user
user = User.objects.create_user("username", "email@example.com", "password")
superuser = User.objects.create_superuser("admin", "admin@example.com", "password")

# Password management
user.set_password("new_password")
user.check_password("password")  # True/False
user.save()

# Permissions
user.has_perm("myapp.can_publish")
user.has_perms(["myapp.can_publish", "myapp.can_edit"])
user.user_permissions.add(permission)
user.groups.add(group)

# Properties
user.is_authenticated  # True for logged-in users
user.is_anonymous      # True for AnonymousUser
user.is_active
user.is_staff
user.is_superuser
```

## Groups and Permissions

```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Create group
editors = Group.objects.create(name="Editors")

# Add permissions to group
content_type = ContentType.objects.get_for_model(Article)
permission = Permission.objects.get(codename="change_article", content_type=content_type)
editors.permissions.add(permission)

# Add user to group
user.groups.add(editors)

# Custom permissions in model
class Article(models.Model):
    class Meta:
        permissions = [
            ("can_publish", "Can publish articles"),
            ("can_feature", "Can feature articles"),
        ]
```

## Template Authentication

```html
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
    <a href="{% url 'logout' %}">Logout</a>
{% else %}
    <a href="{% url 'login' %}">Login</a>
{% endif %}

{% if perms.myapp.can_publish %}
    <a href="{% url 'articles:publish' %}">Publish</a>
{% endif %}
```

## Session Settings

```python
SESSION_ENGINE = "django.contrib.sessions.backends.db"          # database (default)
SESSION_ENGINE = "django.contrib.sessions.backends.cache"       # cache
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"   # cache + DB fallback
SESSION_ENGINE = "django.contrib.sessions.backends.file"        # file-based

SESSION_COOKIE_AGE = 1209600        # 2 weeks (seconds)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_SECURE = True         # HTTPS only
SESSION_COOKIE_HTTPONLY = True        # no JS access
SESSION_COOKIE_SAMESITE = "Lax"
```
