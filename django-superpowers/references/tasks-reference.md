# Django Tasks Framework Reference [6.0+]

The Tasks framework (introduced in Django 6.0) enables running code outside the HTTP request-response cycle. This feature is **only available in Django 6.0 and above**.

## Defining Tasks

```python
# myapp/tasks.py
from django.tasks import task
from django.core.mail import send_mail

@task
def send_welcome_email(user_email, username):
    return send_mail(
        subject="Welcome!",
        message=f"Hello {username}, welcome to our platform.",
        from_email=None,
        recipient_list=[user_email],
    )

# With custom attributes
@task(priority=2, queue_name="emails")
def send_urgent_email(user_email, subject, message):
    return send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[user_email],
    )

# With task context
@task(takes_context=True)
def process_data(context, data_id):
    import logging
    logger = logging.getLogger(__name__)
    logger.debug(
        f"Attempt {context.attempt}, task result id: {context.task_result.id}"
    )
    data = DataModel.objects.get(pk=data_id)
    return process(data)
```

## Enqueueing Tasks

```python
# Sync
result = send_welcome_email.enqueue(user_email="user@example.com", username="John")

# Async
result = await send_welcome_email.aenqueue(user_email="user@example.com", username="John")

# With modified attributes (does not mutate original)
result = send_welcome_email.using(priority=10).enqueue(
    user_email="user@example.com",
    username="John",
)
```

### Serialization Rules

Arguments and return values must be JSON-serializable:
- Strings, integers, floats, booleans, None, lists, dicts are safe.
- Tuples become lists after serialization.
- Datetimes, model instances, and other complex types need manual conversion.

### Enqueueing with Transactions

Avoid workers running tasks before the transaction commits:

```python
from functools import partial
from django.db import transaction

def create_user_view(request):
    with transaction.atomic():
        user = User.objects.create(...)
        transaction.on_commit(partial(
            send_welcome_email.enqueue,
            user_email=user.email,
            username=user.username,
        ))
```

## Task Results

```python
# Get result by ID
result = send_welcome_email.get_result(result_id)

# Or via backend
from django.tasks import default_task_backend
result = default_task_backend.get_result(result_id)

# Async variant
result = await send_welcome_email.aget_result(result_id)

# Refresh result (it's a snapshot)
result.refresh()        # sync
await result.arefresh() # async

# Check status
result.status   # READY, RUNNING, SUCCESSFUL, FAILED

# Get return value (raises ValueError if not finished or failed)
result.return_value

# Get errors (for failed tasks)
result.errors[0].exception_class  # e.g. ValueError
result.errors[0].traceback        # traceback string
```

## Configuration

### TASKS Setting

```python
# settings.py

# Immediate backend (default) - runs tasks synchronously
TASKS = {
    "default": {
        "BACKEND": "django.tasks.backends.immediate.ImmediateBackend",
    }
}

# Dummy backend (testing) - stores but does not run tasks
TASKS = {
    "default": {
        "BACKEND": "django.tasks.backends.dummy.DummyBackend",
    }
}

# Third-party backend (production)
TASKS = {
    "default": {
        "BACKEND": "path.to.production.Backend",
    }
}

# Multiple backends
TASKS = {
    "default": {
        "BACKEND": "path.to.backend",
    },
    "emails": {
        "BACKEND": "path.to.email.backend",
    },
}
```

### Accessing Backends

```python
from django.tasks import default_task_backend, task_backends

backend = default_task_backend          # shortcut for "default"
email_backend = task_backends["emails"] # named backend
```

### Dummy Backend in Tests

```python
from django.tasks import default_task_backend

class TaskTest(TestCase):
    def test_task_enqueued(self):
        send_welcome_email.enqueue(user_email="test@example.com", username="Test")
        self.assertEqual(len(default_task_backend.results), 1)

    def tearDown(self):
        default_task_backend.clear()
```

## Best Practices

1. **Keep task arguments simple**: Use IDs instead of model instances.
2. **Make tasks idempotent**: They may be retried.
3. **Use `transaction.on_commit`**: Ensure data is committed before task runs.
4. **Handle errors gracefully**: Tasks may fail; check `result.errors`.
5. **Define tasks in `tasks.py`**: Convention for discoverability.
6. **Test with DummyBackend**: Verify tasks are enqueued without executing.
