# Generated by Django 3.2.23 on 2024-02-14 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_category_display_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sku',
        ),
    ]
