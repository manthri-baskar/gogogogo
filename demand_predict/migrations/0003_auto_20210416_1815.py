# Generated by Django 3.1.6 on 2021-04-16 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand_predict', '0002_auto_20210416_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods_demand',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
