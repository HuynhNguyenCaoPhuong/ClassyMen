# Generated by Django 4.1.3 on 2023-03-01 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_image_product_img_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
