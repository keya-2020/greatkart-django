# Generated by Django 3.1 on 2021-08-08 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_reviewrating'),
        ('carts', '0011_auto_20210721_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='variation',
            field=models.ManyToManyField(blank=True, to='store.Variation'),
        ),
    ]
