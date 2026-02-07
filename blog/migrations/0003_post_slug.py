from django.db import migrations, models
from django.utils.text import slugify


def populate_unique_slugs(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    for post in Post.objects.all().order_by("id"):
        base = slugify(post.title)[:200] or f"post-{post.id}"
        slug = base
        counter = 2
        while Post.objects.filter(slug=slug).exclude(pk=post.pk).exists():
            suffix = f"-{counter}"
            slug = f"{base[: 200 - len(suffix)]}{suffix}"
            counter += 1
        post.slug = slug
        post.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_content_html_post_content_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=220, null=True),
        ),
        migrations.RunPython(
            code=populate_unique_slugs,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=220, unique=True),
        ),
    ]
