# Generated by Django 3.0.5 on 2021-09-22 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact_forms', '0006_auto_20210921_2311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactintro',
            name='contact_id',
        ),
    ]
