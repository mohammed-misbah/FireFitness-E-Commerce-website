# Generated by Django 4.2.1 on 2024-01-23 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='monthly_sales_report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('product_name', models.CharField(max_length=100, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='sales_report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('product_name', models.CharField(max_length=100, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SalesReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=100)),
                ('categoryName', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('productPrice', models.FloatField()),
            ],
        ),
    ]
