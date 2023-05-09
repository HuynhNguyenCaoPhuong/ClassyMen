# Generated by Django 4.1.3 on 2023-03-04 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_product_category_alter_product_subcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('img_1', models.ImageField(blank=True, default='store/img/img_coming_soon.png', null=True, upload_to='store/img')),
                ('img_2', models.ImageField(blank=True, default='store/img/img_coming_soon.png', null=True, upload_to='store/img')),
                ('img_3', models.ImageField(blank=True, default='store/img/img_coming_soon.png', null=True, upload_to='store/img')),
                ('img_4', models.ImageField(blank=True, default='store/img/img_coming_soon.png', null=True, upload_to='store/img')),
                ('img_5', models.ImageField(blank=True, default='store/img/img_coming_soon.png', null=True, upload_to='store/img')),
                ('img_6', models.ImageField(blank=True, default='store/img/img_coming_soon.png', null=True, upload_to='store/img')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]