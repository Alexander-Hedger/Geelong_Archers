# Generated by Django 3.0.5 on 2020-07-14 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200702_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lifemember',
            name='date_active_end',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='lifemember',
            name='date_active_start',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='lifemember',
            name='long_desc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lifemember',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/users'),
        ),
        migrations.AlterField(
            model_name='lifemember',
            name='short_desc',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='lifemember',
            name='year_made',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]