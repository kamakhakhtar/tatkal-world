# Generated by Django 4.2.5 on 2023-10-15 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0014_varient'),
    ]

    operations = [
        migrations.CreateModel(
            name='Varient_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='varient',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_app.varient_category'),
        ),
    ]