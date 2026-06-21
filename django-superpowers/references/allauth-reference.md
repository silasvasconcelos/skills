---
title: django-allauth Reference
---

# django-allauth Reference

Pinned: `django-allauth[socialaccount,headless,mfa]==65.17.0`. Supports Django 5.2+ (since 65.7.0) and Django 6.0 (since 65.13.1).

## Install

```bash
pip install "django-allauth[socialaccount,headless,mfa]==65.17.0"
```

Trim extras to what you need (`socialaccount`, `headless`, `mfa`). `headless` is **required** for the SPA/mobile API.

## INSTALLED_APPS

```python
INSTALLED_APPS = [
    "django.contrib.sites",  # required; SITE_ID below
    "django.contrib.auth",
    "django.contrib.messages",
    # ...
    "allauth",
    "allauth.account",
    "allauth.headless",          # SPA/mobile API
    "allauth.socialaccount",     # OAuth/OIDC/SAML
    "allauth.socialaccount.providers.google",
    "allauth.mfa",               # TOTP / WebAuthn / recovery codes
]
```

Add `django.template.context_processors.request` to `TEMPLATES[0]["OPTIONS"]["context_processors"]`.

## MIDDLEWARE

```python
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # required
]
```

Do **not** use `SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"`.

## AUTHENTICATION_BACKENDS + Site

```python
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1
```

After `migrate`, ensure `django_site` row `id=1` exists.

## Core account settings

```python
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_PREVENT_ENUMERATION = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APPS": [{
            "client_id": env.str("GOOGLE_OAUTH_CLIENT_ID", default=""),
            "secret": env.str("GOOGLE_OAUTH_SECRET", default=""),
            "key": "",
        }],
    },
}

ACCOUNT_RATE_LIMITS = {
    "login": "30/m/ip",
    "login_failed": "10/m/ip,5/5m/key",
    "signup": "20/m/ip",
    "reset_password": "20/m/ip,5/m/key",
    "confirm_email": "1/3m/key",
}

# Behind reverse proxy (65.14.2+):
# ALLAUTH_TRUSTED_PROXY_COUNT = 1
# ALLAUTH_TRUSTED_CLIENT_IP_HEADER = "HTTP_X_REAL_IP"
```

## URLs

```python
# core/urls.py
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("_allauth/", include("allauth.headless.urls")),
]
```

`HEADLESS_ONLY = True` disables account HTML views but keeps OAuth callbacks under `accounts/`.

## Headless API mode

```python
HEADLESS_ONLY = True

HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": "https://app.example/account/verify-email/{key}",
    "account_reset_password": "https://app.example/account/password/reset",
    "account_reset_password_from_key": "https://app.example/account/password/reset/key/{key}",
    "account_signup": "https://app.example/account/signup",
    "socialaccount_login_error": "https://app.example/account/provider/callback",
}

# Optional: allauth-issued JWTs (alternative to SimpleJWT)
# HEADLESS_TOKEN_STRATEGY = "allauth.headless.tokens.strategies.jwt.JWTTokenStrategy"
# HEADLESS_JWT_ALGORITHM = "RS256"
# HEADLESS_JWT_ACCESS_TOKEN_EXPIRES_IN = 300
# HEADLESS_JWT_REFRESH_TOKEN_EXPIRES_IN = 86400
```

Unauthenticated requests carry `X-Session-Token` against `/_allauth/...` until fully authenticated; then they switch to the long-lived session token or JWT (depending on strategy).

## Integration with DRF + SimpleJWT

| Layer | Role |
|-------|------|
| `allauth.headless` | Signup, login, MFA, email verification, OAuth — owns identity lifecycle |
| `allauth.headless` session token | Optional API auth via `XSessionTokenAuthentication` |
| SimpleJWT (`/api/token/`) | Stateless API auth via `Authorization: Bearer ...` |

**Recommended**: keep allauth headless for account flows and **SimpleJWT for API auth**. After successful headless login, the client requests a JWT pair from `TokenObtainPairView`.

Do not stack `XSessionTokenAuthentication` and `JWTAuthentication` on the same view. Pick one per route.

If you prefer the all-allauth path, set `HEADLESS_TOKEN_STRATEGY` to `JWTTokenStrategy` and use `allauth.headless.contrib.rest_framework.authentication.JWTTokenAuthentication` on DRF views — **do not also install SimpleJWT** in that case.

## Post-install

```bash
python manage.py migrate
```

Create `Site` (admin) and `SocialApp` records (or use settings-based `SOCIALACCOUNT_PROVIDERS`).
