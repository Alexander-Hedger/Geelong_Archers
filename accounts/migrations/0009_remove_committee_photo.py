# Generated by Django 3.0.5 on 2021-09-21 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210921_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='committee',
            name='photo',
        ),
    ]