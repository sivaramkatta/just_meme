# Generated by Django 3.1.4 on 2020-12-30 04:48

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meme', '0006_meme_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='meme',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None),
        ),
    ]
