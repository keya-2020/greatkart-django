# Generated by Django 3.1 on 2021-08-08 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_reviewrating'),
        ('orders', '0003_auto_20210808_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.Variation'),
        ),
    ]
