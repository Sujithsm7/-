# Generated by Django 4.1.5 on 2023-02-20 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0008_productuploadmodel_shopid'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlistm',
            name='userid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
