# Generated by Django 2.1.5 on 2019-04-07 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volt_reservation', '0005_auto_20190407_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventev',
            name='status',
            field=models.CharField(choices=[('AVAILABLE', 'Available'), ('RESERVED', 'Reserved'), ('UNAVAILABLE', 'Unavailable'), ('OUT OF SERVICE', 'Out of Service'), ('COMPLETED', 'Complted')], default='RESERVED', max_length=20),
        ),
        migrations.AlterField(
            model_name='eventcs',
            name='status',
            field=models.CharField(choices=[('AVAILABLE', 'Available'), ('RESERVED', 'Reserved'), ('UNAVAILABLE', 'Unavailable'), ('OUT OF SERVICE', 'Out of Service'), ('COMPLETED', 'Complted')], default='AVAILABLE', max_length=20),
        ),
    ]
