# Generated by Django 4.1.3 on 2022-12-06 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_blog_post_date_alter_comment_comment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='post_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
