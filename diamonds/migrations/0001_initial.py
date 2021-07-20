# Generated by Django 3.2.5 on 2021-07-12 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diamond',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carat', models.FloatField()),
                ('cut', models.CharField(choices=[('Ideal', 'Ideal'), ('Premium', 'Premium'), ('Very_good', 'Very Good'), ('Good', 'Good'), ('fair', 'Fair')], max_length=9)),
                ('color', models.CharField(choices=[('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J')], max_length=1)),
                ('clarity', models.CharField(choices=[('IF', 'IF'), ('VVS1', 'VVS1'), ('VVS2', 'VVS2'), ('VS1', 'VS1'), ('VS2', 'VS2'), ('SI1', 'SI1'), ('SI2', 'SI2'), ('I1', 'I1')], max_length=4)),
                ('depth', models.FloatField()),
                ('table', models.FloatField()),
                ('price', models.BigIntegerField()),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
            ],
        ),
    ]