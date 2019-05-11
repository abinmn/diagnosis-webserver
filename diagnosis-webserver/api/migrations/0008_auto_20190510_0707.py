# Generated by Django 2.1.7 on 2019-05-10 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='pulse_wave_velocity',
            field=models.DecimalField(decimal_places=4, max_digits=5),
        ),
        migrations.AlterField(
            model_name='data',
            name='stiffness_index',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
