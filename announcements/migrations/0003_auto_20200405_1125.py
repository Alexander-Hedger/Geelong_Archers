# Generated by Django 3.0.5 on 2020-04-05 01:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0002_auto_20200405_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='date_published',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]