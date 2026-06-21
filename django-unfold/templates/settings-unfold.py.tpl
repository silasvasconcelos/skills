# settings.py — Unfold configuration scaffold
# Copy relevant sections into your Django settings.
# Docs: https://unfoldadmin.com/docs/configuration/settings/

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    # "unfold.contrib.import_export",
    # "unfold.contrib.simple_history",
    # "unfold.contrib.guardian",
    "django.contrib.admin",
    # ... your apps
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        # ...
    },
]


def dashboard_callback(request, context):
    context.update({
        "cards": [
            {"title": str(_("Users")), "metric": "0"},
            {"title": str(_("Orders")), "metric": "0"},
        ],
    })
    return context


def environment_callback(request):
    return [str(_("Development")), "info"]


def badge_callback(request):
    return 0


def permission_callback(request):
    return request.user.is_authenticated


UNFOLD = {
    "SITE_TITLE": "My Project Admin",
    "SITE_HEADER": "My Project",
    "SITE_SUBHEADER": str(_("Administration")),
    "SITE_URL": "/",
    "SITE_SYMBOL": "dashboard",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": False,
    "ENVIRONMENT": "{{ project }}.callbacks.environment_callback",
    "DASHBOARD_CALLBACK": "{{ project }}.callbacks.dashboard_callback",
    "STYLES": [
        lambda request: static("css/admin-custom.css"),
    ],
    "SCRIPTS": [],
    "BORDER_RADIUS": "6px",
    "LOGIN": {
        "redirect_after": lambda request: reverse_lazy("admin:index"),
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": str(_("Navigation")),
                "separator": True,
                "items": [
                    {
                        "title": str(_("Dashboard")),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
        ],
    },
    "TABS": [
        # {
        #     "models": ["app_label.modelname"],
        #     "items": [
        #         {
        #             "title": str(_("Tab")),
        #             "link": reverse_lazy("admin:app_model_changelist"),
        #             "permission": "{{ project }}.callbacks.permission_callback",
        #         },
        #     ],
        # },
    ],
}

# Replace {{ project }} with your Python package name (e.g. "myapp" or "core").
