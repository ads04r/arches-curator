# Generated by Django 4.2.17 on 2025-04-08 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curator', '0005_curateddataset_ipfs_cid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curateddataset',
            name='search_results',
            field=models.JSONField(default=dict),
        ),
    ]
