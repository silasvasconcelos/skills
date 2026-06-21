# Django Testing Reference (5.0+)

## Test Classes

| Class | Base | Database | Use Case |
|-------|------|----------|----------|
| `SimpleTestCase` | `unittest.TestCase` | No | Views without DB, utilities |
| `TestCase` | `TransactionTestCase` | Yes (transaction wrapped) | Most tests |
| `TransactionTestCase` | `SimpleTestCase` | Yes (real transactions) | Testing transactions |
| `LiveServerTestCase` | `TransactionTestCase` | Yes + live server | Selenium/browser tests |

## Writing Tests

```python
from django.test import TestCase, Client
from django.urls import reverse
from .models import Article

class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up immutable data for the whole TestCase (runs once)."""
        cls.author = User.objects.create_user("testuser", "test@example.com", "password")
        cls.article = Article.objects.create(
            title="Test Article",
            content="Test content",
            author=cls.author,
        )

    def test_str_representation(self):
        self.assertEqual(str(self.article), "Test Article")

    def test_get_absolute_url(self):
        url = self.article.get_absolute_url()
        self.assertEqual(url, f"/articles/{self.article.pk}/")

    def test_title_max_length(self):
        max_length = self.article._meta.get_field("title").max_length
        self.assertEqual(max_length, 200)

    def test_default_ordering(self):
        ordering = Article._meta.ordering
        self.assertEqual(ordering, ["-pub_date"])
```

## View Tests

```python
class ArticleViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("testuser", password="testpass")
        self.article = Article.objects.create(
            title="Test", content="Content", author=self.user,
        )

    def test_list_view_status_code(self):
        response = self.client.get(reverse("articles:list"))
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        response = self.client.get(reverse("articles:list"))
        self.assertTemplateUsed(response, "articles/list.html")

    def test_list_view_contains_article(self):
        response = self.client.get(reverse("articles:list"))
        self.assertContains(response, "Test")

    def test_detail_view(self):
        response = self.client.get(reverse("articles:detail", kwargs={"pk": self.article.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["article"], self.article)

    def test_detail_view_404(self):
        response = self.client.get(reverse("articles:detail", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)

    def test_create_view_requires_login(self):
        response = self.client.get(reverse("articles:create"))
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_create_view_logged_in(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("articles:create"))
        self.assertEqual(response.status_code, 200)

    def test_create_article_post(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("articles:create"), {
            "title": "New Article",
            "content": "New content",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Article.objects.filter(title="New Article").exists())
```

## Form Tests

```python
class ArticleFormTest(TestCase):
    def test_valid_form(self):
        form = ArticleForm(data={
            "title": "Test",
            "content": "Content",
        })
        self.assertTrue(form.is_valid())

    def test_blank_title(self):
        form = ArticleForm(data={"title": "", "content": "Content"})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_title_max_length(self):
        form = ArticleForm(data={"title": "x" * 201, "content": "Content"})
        self.assertFalse(form.is_valid())
```

## Test Client

```python
from django.test import Client

client = Client()

# GET request
response = client.get("/articles/", {"page": "2"})

# POST request
response = client.post("/articles/create/", {"title": "New", "content": "Content"})

# Login
client.login(username="user", password="pass")
client.force_login(user)  # skip authentication backend

# Logout
client.logout()

# Follow redirects
response = client.post("/articles/create/", data, follow=True)

# JSON requests
response = client.post("/api/articles/", data, content_type="application/json")

# File upload
with open("test.txt", "rb") as f:
    response = client.post("/upload/", {"file": f})
```

## Assertion Methods

```python
# Response assertions
self.assertContains(response, "text", count=1, status_code=200)
self.assertNotContains(response, "text")
self.assertTemplateUsed(response, "template.html")
self.assertTemplateNotUsed(response, "other.html")
self.assertRedirects(response, "/expected-url/", status_code=302, target_status_code=200)
self.assertFormError(response.context["form"], "field", ["Error message"])

# JSON response
self.assertJSONEqual(response.content, {"key": "value"})

# HTML
self.assertHTMLEqual(html1, html2)
self.assertInHTML("<p>text</p>", response.content.decode())

# Database
self.assertQuerySetEqual(qs, ["repr1", "repr2"])
self.assertNumQueries(3, lambda: list(Model.objects.all()))
```

## Fixtures and Factory Pattern

```python
# fixtures (JSON/YAML files in app/fixtures/)
class MyTest(TestCase):
    fixtures = ["initial_data.json"]

# Factory pattern (recommended)
class ArticleFactory:
    @staticmethod
    def create(**kwargs):
        defaults = {
            "title": "Test Article",
            "content": "Test content",
        }
        defaults.update(kwargs)
        return Article.objects.create(**defaults)
```

## Testing Settings Override

```python
from django.test import TestCase, override_settings

@override_settings(DEBUG=True, CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}})
class MyTest(TestCase):
    def test_something(self):
        ...

    @override_settings(LANGUAGE_CODE="pt-br")
    def test_translation(self):
        ...
```

## Testing Email

```python
from django.core import mail

class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail("Subject", "Body", "from@example.com", ["to@example.com"])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Subject")
```

## Async Testing

```python
from django.test import TestCase

class AsyncViewTest(TestCase):
    async def test_async_view(self):
        response = await self.async_client.get("/async-endpoint/")
        self.assertEqual(response.status_code, 200)
```

## Running Tests

```bash
# All tests
python manage.py test

# Specific app
python manage.py test myapp

# Specific test class
python manage.py test myapp.tests.ArticleModelTest

# Specific test method
python manage.py test myapp.tests.ArticleModelTest.test_str_representation

# Verbosity
python manage.py test --verbosity=2

# Parallel
python manage.py test --parallel

# Fail fast
python manage.py test --failfast

# With coverage
coverage run manage.py test
coverage report
coverage html
```
