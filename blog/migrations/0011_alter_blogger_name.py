# Generated by Django 4.1.3 on 2022-12-07 18:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0010_alter_blog_post_date_alter_comment_comment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogger',
            name='name',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]