# Generated by Django 4.2.5 on 2023-11-02 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0020_seo_blog_seo_product_seo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='card_images/')),
                ('title', models.CharField(max_length=200)),
                ('discount_percentage', models.PositiveIntegerField()),
                ('call_to_action_link', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='carousel_images/')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(max_length=200)),
                ('page_link', models.CharField(max_length=200)),
                ('discount_percentage', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='IndexPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cards', models.ManyToManyField(related_name='index_page_cards', to='store_app.card')),
                ('carousels', models.ManyToManyField(related_name='index_page_carousels', to='store_app.carousel')),
                ('selected_blogs', models.ManyToManyField(related_name='index_page_selected_blogs', to='store_app.blog')),
                ('selected_products', models.ManyToManyField(related_name='index_page_selected_products', to='store_app.product')),
            ],
        ),
    ]
