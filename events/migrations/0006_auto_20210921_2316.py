# Generated by Django 3.0.5 on 2021-09-21 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_eventcomp_event_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventintro',
            name='current_lh',
        ),
        migrations.RemoveField(
            model_name='eventintro',
            name='max_lh',
        ),
    ]
