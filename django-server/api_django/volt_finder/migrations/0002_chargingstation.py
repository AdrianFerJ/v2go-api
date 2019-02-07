# Generated by Django 2.1.5 on 2019-02-07 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volt_finder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargingStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nk', models.CharField(db_index=True, max_length=32, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('location', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('AVAILABLE', 'AVAILABLE'), ('RESERVED', 'RESERVED'), ('UNAVAILABLE', 'UNAVAILABLE'), ('OUT_OF_SERVICE', 'OUT_OF_SERVICE')], default='UNAVAILABLE', max_length=20)),
                ('manager_id', models.IntegerField()),
            ],
        ),
    ]
