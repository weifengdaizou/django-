# Generated by Django 4.2.9 on 2024-03-15 21:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0002_alter_article_comment_count_alter_article_content_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
