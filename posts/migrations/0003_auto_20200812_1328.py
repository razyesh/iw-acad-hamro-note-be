# Generated by Django 3.1 on 2020-08-12 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200811_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_slug',
            field=models.SlugField(unique=True),
        ),
    ]
