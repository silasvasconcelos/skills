# admin.py — Custom Unfold admin page
# Register a custom view under a ModelAdmin.

from django.urls import path
from django.views.generic import TemplateView
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.views import UnfoldModelAdminViewMixin

from {{ app }}.models import {{ Model }}


class {{ Model }}ReportView(UnfoldModelAdminViewMixin, TemplateView):
    title = "{{ Model }} Report"
    permission_required = ("{{ app }}.view_{{ model }}",)
    template_name = "admin/{{ app }}/{{ model }}_report.html"


@admin.register({{ Model }})
class {{ Model }}Admin(ModelAdmin):
    def get_urls(self):
        report_view = self.admin_site.admin_view(
            {{ Model }}ReportView.as_view(model_admin=self)
        )
        return super().get_urls() + [
            path("report/", report_view, name="{{ app }}_{{ model }}_report"),
        ]

# Add to UNFOLD["SIDEBAR"]["navigation"] manually:
# {
#     "title": "Report",
#     "icon": "analytics",
#     "link": reverse_lazy("admin:{{ app }}_{{ model }}_report"),
# }
