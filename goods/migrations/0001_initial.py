# Generated by Django 3.1.6 on 2021-03-13 02:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import goods.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0004_auto_20210313_0814'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_req', models.FloatField(validators=[goods.models.validate_positive])),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('good_name', models.CharField(max_length=100)),
                ('setup_cost', models.FloatField(help_text='Rs./run', validators=[goods.models.validate_positive])),
                ('prod_cost', models.FloatField(help_text='Rs./unit', validators=[goods.models.validate_positive])),
                ('hold_cost', models.FloatField(help_text='Rs./unit-year', validators=[goods.models.validate_positive])),
                ('prod_rate', models.FloatField(help_text='units/year', validators=[goods.models.validate_positive])),
                ('prod_quantity', models.FloatField(help_text='units/run', validators=[goods.models.validate_positive])),
                ('raw_material', models.ManyToManyField(through='goods.Amount', to='products.Product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='good', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='amount',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goods'),
        ),
        migrations.AddField(
            model_name='amount',
            name='prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]
