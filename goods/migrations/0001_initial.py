# Generated by Django 3.1.6 on 2021-04-25 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import goods.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Amount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('required_amount', models.FloatField(validators=[goods.models.validate_positive])),
            ],
        ),
        migrations.CreateModel(
            name='goods_demand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=220)),
                ('date', models.DateTimeField()),
                ('demand', models.PositiveIntegerField()),
                ('place', models.CharField(default='rayachoty', max_length=220)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='good_demand', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('good_name', models.CharField(max_length=100)),
                ('setup_cost', models.FloatField(help_text='Rs./run', validators=[goods.models.validate_positive])),
                ('production_cost', models.FloatField(help_text='Rs./unit', validators=[goods.models.validate_positive])),
                ('holding_cost', models.FloatField(help_text='Rs./unit-year', validators=[goods.models.validate_positive])),
                ('production_rate', models.FloatField(help_text='units/year', validators=[goods.models.validate_positive])),
                ('total_demand', models.FloatField(help_text='units/year', validators=[goods.models.validate_positive])),
                ('production_quantity', models.FloatField(help_text='units/run', validators=[goods.models.validate_positive])),
                ('raw_material', models.ManyToManyField(through='goods.Amount', to='products.Product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='good', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='company_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=220)),
                ('periods', models.PositiveIntegerField()),
                ('level_sc', models.FloatField()),
                ('trend_sc', models.FloatField()),
                ('seasonal_factor_sc', models.FloatField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='amount',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goods'),
        ),
        migrations.AddField(
            model_name='amount',
            name='raw_mate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AddField(
            model_name='amount',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='amount', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='amount',
            unique_together={('goods', 'raw_mate')},
        ),
    ]
