# Generated by Django 3.1.6 on 2021-04-25 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=220)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('lead_time', models.PositiveIntegerField(blank=True, default='0', null=True, validators=[products.models.validate_zero])),
                ('service_level', models.PositiveIntegerField(blank=True, default='90', null=True, validators=[products.models.validate_even])),
                ('standard_deviation', models.DecimalField(blank=True, decimal_places=3, default='5', max_digits=10, null=True)),
                ('carrying_cost', models.PositiveIntegerField(default='12', help_text='Enter as percentage of unit cost', validators=[products.models.validate_even])),
                ('ordering_cost', models.PositiveIntegerField(default='0', null=True)),
                ('unit_costprice', models.PositiveIntegerField(default='0', null=True, validators=[products.models.validate_zero])),
                ('average_daily_demand', models.DecimalField(decimal_places=3, default='0', max_digits=10, null=True)),
                ('total_inventory', models.IntegerField(blank=True, default='0', null=True)),
                ('eoq', models.IntegerField(blank=True, default='0', null=True)),
                ('no_of_workingdays', models.IntegerField(blank=True, default='300', null=True)),
                ('rq', models.IntegerField(blank=True, default='0', null=True)),
                ('z', models.DecimalField(blank=True, decimal_places=3, default='0', max_digits=4, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(null=True)),
                ('quantity', models.IntegerField(null=True)),
                ('total_price', models.PositiveIntegerField(blank=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('recieved', models.IntegerField(default='0', null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demands', to='products.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='demand', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
