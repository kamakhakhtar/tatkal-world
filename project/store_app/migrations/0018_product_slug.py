# Generated by Django 4.2.5 on 2023-10-15 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0017_remove_product_varient_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=200, null=True),
        ),
    ]
