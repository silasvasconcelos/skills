{# templates/admin/index.html — Custom Unfold dashboard #}
{# Requires UNFOLD["DASHBOARD_CALLBACK"] to inject context variables #}
{% extends "admin/base.html" %}

{% load i18n unfold %}

{% block title %}
    {% if subtitle %}{{ subtitle }} | {% endif %}
    {{ title }} | {{ site_title|default:_('Django site admin') }}
{% endblock %}

{% block branding %}
    {% include "unfold/helpers/site_branding.html" %}
{% endblock %}

{% block content %}
{% component "unfold/components/container.html" %}
    <div class="flex flex-col gap-6">
        {# Metric cards — pass `cards` from DASHBOARD_CALLBACK #}
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            {% for card in cards %}
                {% component "unfold/components/card.html" %}
                    {% component "unfold/components/text.html" %}
                        {{ card.title }}
                    {% endcomponent %}
                    {% component "unfold/components/title.html" %}
                        {{ card.metric }}
                    {% endcomponent %}
                {% endcomponent %}
            {% empty %}
                {% component "unfold/components/card.html" %}
                    {% component "unfold/components/text.html" %}
                        {% trans "Configure DASHBOARD_CALLBACK to inject cards." %}
                    {% endcomponent %}
                {% endcomponent %}
            {% endfor %}
        </div>

        {# Optional navigation links — pass `navigation` from callback #}
        {% if navigation %}
            {% component "unfold/components/navigation.html" with items=navigation %}
            {% endcomponent %}
        {% endif %}
    </div>
{% endcomponent %}
{% endblock %}
