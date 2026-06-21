# admin.py — Feature-rich Unfold ModelAdmin template
# Replace {{ app }} and {{ Model }} with your app/model names.

from django.contrib import admin
from django.db import models
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import action, display
from unfold.enums import ActionVariant
from unfold.contrib.filters.admin import FieldTextFilter, RangeDateFilter, ChoicesDropdownFilter
from unfold.contrib.forms.widgets import WysiwygWidget

from {{ app }}.models import {{ Model }}


@admin.register({{ Model }})
class {{ Model }}Admin(ModelAdmin):
    # Changelist
    list_display = ["name_display", "status_display", "created_at"]
    list_filter_submit = True
    list_filter = [
        ("name", FieldTextFilter),
        ("status", ChoicesDropdownFilter),
        ("created_at", RangeDateFilter),
    ]
    search_fields = ["name"]
    list_per_page = 25
    ordering = ["-created_at"]

    # Changeform
    compressed_fields = True
    warn_unsaved_form = True
    change_form_show_cancel_button = True
    readonly_fields = ["created_at", "updated_at"]

    # Actions
    actions_list = []
    actions_row = []
    actions_detail = []
    actions_submit_line = []

    # Sortable (requires weight PositiveIntegerField on model)
    # ordering_field = "weight"
    # hide_ordering_field = True

    # Widgets
    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
    }

    @display(description=_("Name"), header=True)
    def name_display(self, obj):
        return [obj.name, str(obj.pk)]

    @display(
        description=_("Status"),
        label={"active": "success", "inactive": "danger"},
    )
    def status_display(self, obj):
        return obj.status

    # Example action — uncomment and customize
    # @action(description=_("Archive"), icon="archive", variant=ActionVariant.WARNING)
    # def archive(self, request, object_id: int):
    #     obj = self.model.objects.get(pk=object_id)
    #     obj.is_archived = True
    #     obj.save()
    #     return redirect("admin:{{ app }}_{{ model }}_change", object_id)
