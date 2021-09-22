# Generated by Django 3.0.5 on 2021-09-21 13:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contact_forms', '0004_contactintro_contact_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactintro',
            name='contact_id',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=100),
        ),
    ]
