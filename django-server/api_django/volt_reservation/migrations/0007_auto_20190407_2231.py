# Generated by Django 2.1.5 on 2019-04-07 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volt_reservation', '0006_auto_20190407_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcs',
            name='status',
            field=models.CharField(choices=[('AVAILABLE', 'Available'), ('RESERVED', 'Reserved'), ('UNAVAILABLE', 'Unavailable'), ('OUT OF SERVICE', 'Out of Service'), ('COMPLETED', 'Complted'), ('CANCELED', 'Canceled')], default='AVAILABLE', max_length=20),
        ),
        migrations.AlterField(
            model_name='eventev',
            name='status',
            field=models.CharField(choices=[('AVAILABLE', 'Available'), ('RESERVED', 'Reserved'), ('UNAVAILABLE', 'Unavailable'), ('OUT OF SERVICE', 'Out of Service'), ('COMPLETED', 'Complted'), ('CANCELED', 'Canceled')], default='RESERVED', max_length=20),
        ),
    ]
