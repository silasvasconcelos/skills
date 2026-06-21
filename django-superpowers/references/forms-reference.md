# Django Forms Reference (5.0+)

## Form Definition

```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False)
```

## ModelForm

```python
from django.forms import ModelForm
from .models import Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "tags"]       # explicit list (recommended)
        # fields = "__all__"                         # all fields (avoid in production)
        # exclude = ["author"]                       # exclude specific fields
        widgets = {
            "content": forms.Textarea(attrs={"rows": 10, "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Article Title",
        }
        help_texts = {
            "tags": "Comma-separated tags.",
        }
        error_messages = {
            "title": {"max_length": "Title is too long."},
        }
```

### ModelForm save()

```python
# Create new
form = ArticleForm(request.POST)
if form.is_valid():
    article = form.save()

# Update existing
article = Article.objects.get(pk=1)
form = ArticleForm(request.POST, instance=article)
if form.is_valid():
    article = form.save()

# Deferred save
article = form.save(commit=False)
article.author = request.user
article.save()
form.save_m2m()  # required for M2M when commit=False
```

### modelform_factory

```python
from django.forms import modelform_factory

ArticleForm = modelform_factory(Article, fields=["title", "content"])
ArticleForm = modelform_factory(Article, exclude=["created_at"])
```

## Form Fields

| Field | HTML Widget | Key Arguments |
|-------|-------------|---------------|
| `CharField` | `<input type="text">` | `max_length`, `min_length`, `strip` |
| `EmailField` | `<input type="email">` | - |
| `URLField` | `<input type="url">` | - |
| `IntegerField` | `<input type="number">` | `min_value`, `max_value` |
| `FloatField` | `<input type="number">` | - |
| `DecimalField` | `<input type="number">` | `max_digits`, `decimal_places` |
| `BooleanField` | `<input type="checkbox">` | - |
| `DateField` | `<input type="text">` | `input_formats` |
| `DateTimeField` | `<input type="text">` | `input_formats` |
| `TimeField` | `<input type="text">` | `input_formats` |
| `ChoiceField` | `<select>` | `choices` |
| `MultipleChoiceField` | `<select multiple>` | `choices` |
| `TypedChoiceField` | `<select>` | `choices`, `coerce` |
| `FileField` | `<input type="file">` | `max_length`, `allow_empty_file` |
| `ImageField` | `<input type="file">` | - |
| `ModelChoiceField` | `<select>` | `queryset` |
| `ModelMultipleChoiceField` | `<select multiple>` | `queryset` |
| `SlugField` | `<input type="text">` | `allow_unicode` |
| `UUIDField` | `<input type="text">` | - |
| `JSONField` | `<textarea>` | `encoder`, `decoder` |

## Widgets

```python
from django import forms

class MyForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 40}))
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    choice = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    multi = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CHOICES)
    password = forms.CharField(widget=forms.PasswordInput)
    hidden = forms.CharField(widget=forms.HiddenInput)
```

## Form Validation

### Field-level validation

```python
class MyForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email.endswith("@example.com"):
            raise forms.ValidationError("Must use example.com email.")
        return email
```

### Form-level validation

```python
class SignupForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get("password")
        pw2 = cleaned_data.get("password_confirm")
        if pw and pw2 and pw != pw2:
            raise forms.ValidationError("Passwords do not match.")
```

### Custom validators

```python
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Enter a valid phone number.",
)

class ContactForm(forms.Form):
    phone = forms.CharField(validators=[phone_validator])
```

## Formsets

```python
from django.forms import formset_factory

ArticleFormSet = formset_factory(ArticleForm, extra=3, max_num=10, can_delete=True)

# In view
if request.method == "POST":
    formset = ArticleFormSet(request.POST)
    if formset.is_valid():
        for form in formset:
            if form.cleaned_data and not form.cleaned_data.get("DELETE"):
                form.save()
else:
    formset = ArticleFormSet()
```

### Model Formsets

```python
from django.forms import modelformset_factory

ArticleFormSet = modelformset_factory(Article, fields=["title", "content"], extra=1)
formset = ArticleFormSet(queryset=Article.objects.filter(author=request.user))
```

### Inline Formsets

```python
from django.forms import inlineformset_factory

BookFormSet = inlineformset_factory(Author, Book, fields=["title"], extra=2)
formset = BookFormSet(instance=author)
```

## Rendering Forms in Templates

```html
{# Full form #}
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>

{# Render options #}
{{ form.as_p }}        {# Wrapped in <p> tags #}
{{ form.as_div }}      {# Wrapped in <div> tags (default in 5.0+) #}
{{ form.as_table }}    {# Wrapped in <tr> tags #}
{{ form.as_ul }}       {# Wrapped in <li> tags #}

{# Manual field rendering #}
<form method="post">
    {% csrf_token %}
    {% for field in form %}
        <div class="field {% if field.errors %}has-error{% endif %}">
            {{ field.label_tag }}
            {{ field }}
            {% if field.help_text %}<small>{{ field.help_text }}</small>{% endif %}
            {% for error in field.errors %}<span class="error">{{ error }}</span>{% endfor %}
        </div>
    {% endfor %}
    {{ form.non_field_errors }}
    <button type="submit">Submit</button>
</form>

{# Individual field access #}
{{ form.email }}
{{ form.email.label_tag }}
{{ form.email.errors }}
{{ form.email.value }}
{{ form.email.id_for_label }}
```

## Field Group Template Rendering [5.0+]

Individual form fields can be rendered with their label, help text, and errors using `as_field_group()`:

```html
<form method="post">
    {% csrf_token %}
    {{ form.name.as_field_group }}
    {{ form.email.as_field_group }}
    {{ form.message.as_field_group }}
    <button type="submit">Submit</button>
</form>
```

This renders each field wrapped in a `<div>` with its label, widget, help text, and errors — replacing the need for manual field rendering loops in most cases.

## File Upload Form

```python
class UploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

# Template must use enctype
# <form method="post" enctype="multipart/form-data">

# View must pass request.FILES
form = UploadForm(request.POST, request.FILES)
```
