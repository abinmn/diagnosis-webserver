# Generated by Django 2.1.7 on 2019-05-11 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_data_plot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='plot',
            field=models.ImageField(upload_to=''),
        ),
    ]
