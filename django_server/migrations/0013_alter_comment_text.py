# Generated by Django 4.2.3 on 2023-08-18 18:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("django_server", "0012_alter_postscore_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="text",
            field=models.TextField(max_length=65535),
        ),
    ]