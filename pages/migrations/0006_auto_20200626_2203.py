# Generated by Django 3.0.5 on 2020-06-26 12:03

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20200626_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagecontent',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
    ]