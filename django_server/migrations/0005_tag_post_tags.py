# Generated by Django 5.0.1 on 2024-03-16 17:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("django_server", "0004_tag2_remove_post_tags_delete_tag"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(blank=True, to="django_server.tag"),
        ),
    ]
