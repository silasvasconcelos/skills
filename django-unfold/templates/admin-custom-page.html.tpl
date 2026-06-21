{# templates/admin/{{ app }}/{{ model }}_report.html #}
{% extends "admin/base.html" %}

{% load i18n unfold %}

{% block content %}
    {% tab_list "{{ app }}" %}

    {% component "unfold/components/container.html" %}
        {% component "unfold/components/title.html" %}
            {% trans "Report" %}
        {% endcomponent %}

        {% component "unfold/components/text.html" %}
            {% trans "Custom admin page content goes here." %}
        {% endcomponent %}
    {% endcomponent %}
{% endblock %}
