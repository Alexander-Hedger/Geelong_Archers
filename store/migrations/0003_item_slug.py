# Generated by Django 3.0.5 on 2020-06-28 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_item_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='test-1'),
            preserve_default=False,
        ),
    ]
