# Generated by Django 5.0.1 on 2024-03-16 17:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("django_server", "0003_post_tags"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="tags",
        ),
        migrations.DeleteModel(
            name="Tag",
        ),
    ]
