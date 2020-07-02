# Generated by Django 3.0.5 on 2020-04-14 05:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgmMinutes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_published', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('minutes', models.FileField(upload_to='docs/agm_minutes/%Y')),
            ],
        ),
        migrations.CreateModel(
            name='CommitteeMinutes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_published', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('minutes', models.FileField(upload_to='docs/committee_minutes/%Y')),
            ],
        ),
    ]