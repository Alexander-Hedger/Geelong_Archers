# Generated by Django 3.0.5 on 2020-07-03 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20200626_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagecontent',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]