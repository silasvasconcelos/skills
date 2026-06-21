# Django Migrations Reference (5.0+)

## Workflow

```bash
# 1. Edit models.py
# 2. Create migration
python manage.py makemigrations
python manage.py makemigrations myapp

# 3. Review migration (optional)
python manage.py sqlmigrate myapp 0001

# 4. Apply migration
python manage.py migrate
python manage.py migrate myapp

# Check status
python manage.py showmigrations
python manage.py showmigrations --plan
```

## Common Commands

```bash
# Create empty migration (for data migrations or RunSQL)
python manage.py makemigrations myapp --empty --name describe_change

# Reverse a migration
python manage.py migrate myapp 0003       # migrate back to 0003
python manage.py migrate myapp zero       # unapply all

# Squash migrations
python manage.py squashmigrations myapp 0001 0010

# Check for migration issues
python manage.py makemigrations --check    # exit 1 if migrations needed
python manage.py migrate --check           # exit 1 if unapplied migrations

# Dry run
python manage.py migrate --plan

# Merge conflicting migrations
python manage.py makemigrations --merge
```

## Migration Operations

```python
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        # Schema operations
        migrations.CreateModel(
            name="Article",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True)),
                ("title", models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name="article",
            name="content",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="article",
            name="title",
            field=models.CharField(max_length=300),
        ),
        migrations.RemoveField(
            model_name="article",
            name="old_field",
        ),
        migrations.RenameField(
            model_name="article",
            old_name="title",
            new_name="headline",
        ),
        migrations.RenameModel(
            old_name="Article",
            new_name="Post",
        ),
        migrations.DeleteModel(
            name="OldModel",
        ),
        migrations.AddIndex(
            model_name="article",
            index=models.Index(fields=["pub_date"], name="pub_date_idx"),
        ),
        migrations.AddConstraint(
            model_name="article",
            constraint=models.UniqueConstraint(
                fields=["author", "title"], name="unique_author_title"
            ),
        ),
        migrations.AlterModelOptions(
            name="article",
            options={"ordering": ["-pub_date"]},
        ),
    ]
```

## Data Migrations

```python
from django.db import migrations

def populate_slug(apps, schema_editor):
    """Forward migration: populate slug from title."""
    Article = apps.get_model("myapp", "Article")
    from django.utils.text import slugify
    for article in Article.objects.all():
        article.slug = slugify(article.title)
        article.save(update_fields=["slug"])

def reverse_populate_slug(apps, schema_editor):
    """Reverse migration: clear slug field."""
    Article = apps.get_model("myapp", "Article")
    Article.objects.all().update(slug="")

class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_article_slug"),
    ]

    operations = [
        migrations.RunPython(populate_slug, reverse_populate_slug),
    ]
```

## RunSQL

```python
class Migration(migrations.Migration):
    dependencies = [("myapp", "0001_initial")]

    operations = [
        migrations.RunSQL(
            sql="CREATE INDEX myapp_article_title_idx ON myapp_article (title);",
            reverse_sql="DROP INDEX myapp_article_title_idx;",
        ),
    ]
```

## SeparateDatabaseAndState

```python
# Rename a table without Django thinking the model was deleted and recreated
migrations.SeparateDatabaseAndState(
    state_operations=[
        migrations.RenameModel(
            old_name="OldName",
            new_name="NewName",
        ),
    ],
    database_operations=[
        migrations.RunSQL(
            sql="ALTER TABLE myapp_oldname RENAME TO myapp_newname;",
            reverse_sql="ALTER TABLE myapp_newname RENAME TO myapp_oldname;",
        ),
    ],
)
```

## Adding Non-Nullable Field

Three approaches:

```python
# Option 1: Provide a default
content = models.TextField(default="")

# Option 2: Allow null temporarily, then fill, then remove null
# Migration 1: AddField with null=True
# Migration 2: RunPython to fill values
# Migration 3: AlterField to null=False

# Option 3: Interactive default during makemigrations
# Django will ask for a one-off default
```

## Migration Dependencies

```python
class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0001_initial"),
        ("other_app", "0005_auto"),  # cross-app dependency
    ]
    run_before = [
        ("other_app", "0006_something"),  # ensure this runs before
    ]
```

## Best Practices

1. **NEVER generate migration files from AI** — migrations MUST only be created via `python manage.py makemigrations`. The AI may instruct the user to run the command but MUST NOT write or edit migration files directly.
2. **Always commit migrations** to version control.
3. **Never edit applied migrations** in production.
4. **Use `--check` in CI** to ensure no missing migrations.
5. **Squash periodically** to reduce migration count.
6. **Test migrations** both forward and backward.
7. **Use `apps.get_model()`** in data migrations, never import models directly.
8. **Always provide `reverse_code`** for `RunPython` operations.
9. **Review generated SQL** with `sqlmigrate` before applying.
