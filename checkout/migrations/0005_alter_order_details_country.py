# Generated by Django 3.2.23 on 2024-03-05 15:00

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_alter_order_details_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_details',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
