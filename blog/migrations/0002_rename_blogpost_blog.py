# Generated by Django 4.1.3 on 2022-11-22 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BlogPost',
            new_name='Blog',
        ),
    ]
