# Generated by Django 3.0.5 on 2020-04-23 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0003_memberevents_total_awards'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberClassification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('rank', models.IntegerField()),
                ('discipline', models.CharField(max_length=20)),
                ('archer_class', models.CharField(max_length=20)),
                ('division', models.CharField(max_length=30)),
                ('classification', models.CharField(max_length=30)),
                ('score_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MemberClassificationAnnual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('rank', models.IntegerField()),
                ('discipline', models.CharField(max_length=20)),
                ('archer_class', models.CharField(max_length=20)),
                ('division', models.CharField(max_length=30)),
                ('classification', models.CharField(max_length=30)),
                ('score_count', models.IntegerField()),
                ('year', models.IntegerField()),
            ],
        ),
    ]