# Generated by Django 4.1.5 on 2023-02-20 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0009_wishlistm_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartm',
            name='userid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
