# Generated by Django 3.1.2 on 2021-06-26 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_delete_varaiationmanager'),
        ('carts', '0004_auto_20210622_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='variation',
            field=models.ManyToManyField(blank=True, to='store.Variation'),
        ),
    ]