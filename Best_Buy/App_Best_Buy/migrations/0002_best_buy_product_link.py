# Generated by Django 3.1 on 2020-08-26 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Best_Buy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='best_buy',
            name='product_link',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]
