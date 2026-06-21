# Django Templates Reference (5.0+)

## Template Language

### Variables

```html
{{ variable }}
{{ object.attribute }}
{{ dict.key }}
{{ list.0 }}
{{ object.method }}
```

### Tags

```html
{% if condition %}...{% elif other %}...{% else %}...{% endif %}
{% for item in list %}...{% empty %}No items{% endfor %}
{% block name %}...{% endblock %}
{% extends "base.html" %}
{% include "partial.html" %}
{% include "partial.html" with title="Hello" only %}
{% load static %}
{% url 'name' arg1 arg2 %}
{% csrf_token %}
{% comment %}...{% endcomment %}
{% spaceless %}...{% endspaceless %}
{% verbatim %}...{% endverbatim %}
{% with total=business.employees.count %}...{% endwith %}
{% cycle 'odd' 'even' %}
{% now "Y-m-d H:i" %}
{% regroup list by attribute as grouped %}
{% lorem 2 p %}
```

### For Loop Variables

```html
{% for item in list %}
    {{ forloop.counter }}      {# 1-indexed #}
    {{ forloop.counter0 }}     {# 0-indexed #}
    {{ forloop.revcounter }}   {# reverse counter #}
    {{ forloop.first }}        {# True for first iteration #}
    {{ forloop.last }}         {# True for last iteration #}
    {{ forloop.parentloop }}   {# parent loop (nested) #}
{% endfor %}
```

### Filters

```html
{{ value|default:"nothing" }}
{{ value|default_if_none:"N/A" }}
{{ value|length }}
{{ value|lower }}
{{ value|upper }}
{{ value|title }}
{{ value|capfirst }}
{{ value|truncatewords:30 }}
{{ value|truncatechars:100 }}
{{ value|striptags }}
{{ value|linebreaks }}
{{ value|linebreaksbr }}
{{ value|escape }}
{{ value|safe }}
{{ value|urlencode }}
{{ value|slugify }}
{{ value|yesno:"yes,no,maybe" }}

{# Date/time #}
{{ value|date:"F j, Y" }}
{{ value|date:"Y-m-d" }}
{{ value|time:"H:i" }}
{{ value|timesince }}
{{ value|timeuntil }}

{# Numbers #}
{{ value|floatformat:2 }}
{{ value|filesizeformat }}
{{ value|add:5 }}
{{ value|divisibleby:3 }}

{# Lists #}
{{ list|join:", " }}
{{ list|first }}
{{ list|last }}
{{ list|slice:":5" }}
{{ list|dictsort:"name" }}
{{ list|dictsortreversed:"name" }}
{{ list|unordered_list }}

{# Strings #}
{{ value|cut:" " }}
{{ value|wordcount }}
{{ value|wordwrap:80 }}
{{ value|center:15 }}
{{ value|ljust:15 }}
{{ value|rjust:15 }}

{# JSON #}
{{ value|json_script:"data-id" }}

{# Pluralize #}
{{ count }} item{{ count|pluralize }}
{{ count }} categor{{ count|pluralize:"y,ies" }}
```

## Template Inheritance

```html
{# base.html #}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{% block title %}My Site{% endblock %}</title>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>{% block header %}{% endblock %}</header>
    <main>{% block content %}{% endblock %}</main>
    <footer>{% block footer %}{% endblock %}</footer>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

```html
{# page.html #}
{% extends "base.html" %}

{% block title %}My Page - {{ block.super }}{% endblock %}

{% block content %}
<h1>Hello World</h1>
{% endblock %}
```

## Static Files

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/app.js' %}"></script>
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

## querystring Tag [5.1+]

Build and modify query strings in templates without manual URL encoding. Preserves existing query parameters by default.

```html
{% load querystring %}

{# Add/replace query parameters #}
<a href="{% querystring page=2 %}">Page 2</a>

{# Preserve existing params while modifying one #}
<a href="{% querystring page=page_obj.next_page_number %}">Next</a>

{# Remove a parameter by setting to None #}
<a href="{% querystring page=None %}">Remove page param</a>

{# Multiple parameters #}
<a href="{% querystring page=1 sort="title" %}">Sort by title</a>
```

## URL Tag

```html
{% url 'app:view-name' %}
{% url 'app:view-name' pk=object.pk %}
{% url 'app:view-name' object.pk %}

{# Store in variable #}
{% url 'app:view-name' pk=object.pk as detail_url %}
<a href="{{ detail_url }}">Link</a>
```

## Conditional Tags

```html
{% if user.is_authenticated %}
    Welcome, {{ user.username }}!
{% elif user.is_anonymous %}
    Please log in.
{% else %}
    Unknown state.
{% endif %}

{# Operators: and, or, not, ==, !=, <, >, <=, >=, in, not in, is, is not #}
{% if article.status == "published" and article.author == user %}
    <a href="{% url 'edit' article.pk %}">Edit</a>
{% endif %}

{% if "python" in article.tags.all %}
    Python article!
{% endif %}
```

## Form Rendering

```html
{# Auto-render #}
{{ form.as_div }}
{{ form.as_p }}
{{ form.as_table }}

{# Manual rendering #}
{% for field in form %}
<div class="form-group{% if field.errors %} has-error{% endif %}">
    <label for="{{ field.id_for_label }}">{{ field.label }}</label>
    {{ field }}
    {% if field.help_text %}<small>{{ field.help_text }}</small>{% endif %}
    {% for error in field.errors %}<span class="error">{{ error }}</span>{% endfor %}
</div>
{% endfor %}

{# Non-field errors #}
{% if form.non_field_errors %}
<div class="errors">
    {% for error in form.non_field_errors %}
    <p>{{ error }}</p>
    {% endfor %}
</div>
{% endif %}
```

## Messages Framework

```html
{% if messages %}
<div class="messages">
    {% for message in messages %}
    <div class="alert alert-{{ message.tags }}">
        {{ message }}
    </div>
    {% endfor %}
</div>
{% endif %}
```

```python
# In views
from django.contrib import messages

messages.debug(request, "Debug message")
messages.info(request, "Info message")
messages.success(request, "Success message")
messages.warning(request, "Warning message")
messages.error(request, "Error message")
```

## Pagination

```html
{% for article in page_obj %}
    <h2>{{ article.title }}</h2>
{% endfor %}

<nav>
    {% if page_obj.has_previous %}
        <a href="?page=1">First</a>
        <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
    {% endif %}

    Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}

    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">Next</a>
        <a href="?page={{ page_obj.paginator.num_pages }}">Last</a>
    {% endif %}
</nav>
```

## Custom Template Tags and Filters

```python
# myapp/templatetags/myapp_tags.py
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.simple_tag
def current_time(format_string):
    from django.utils import timezone
    return timezone.now().strftime(format_string)

@register.simple_tag(takes_context=True)
def greeting(context):
    user = context["request"].user
    return f"Hello, {user.username}!"

@register.inclusion_tag("myapp/sidebar.html", takes_context=True)
def sidebar(context):
    return {"articles": Article.objects.all()[:5]}
```

```html
{% load myapp_tags %}
{{ price|multiply:1.2 }}
{% current_time "%Y-%m-%d" %}
{% greeting %}
{% sidebar %}
```

## Template Configuration

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],   # project-level templates
        "APP_DIRS": True,                    # app-level templates/<app>/
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "myapp.context_processors.my_custom_processor",
            ],
        },
    },
]
```

### Custom Context Processor

```python
# myapp/context_processors.py
def site_settings(request):
    return {
        "SITE_NAME": "My Site",
        "SITE_URL": "https://example.com",
    }
```
