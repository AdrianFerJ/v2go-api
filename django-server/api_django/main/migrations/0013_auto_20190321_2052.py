# Generated by Django 2.1.5 on 2019-03-21 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20190320_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chargingstation',
            name='nk',
            field=models.CharField(db_index=True, max_length=32, unique=True),
        ),
    ]
