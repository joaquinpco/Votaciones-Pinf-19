# Generated by Django 2.2 on 2019-11-19 18:49

import VotacionesUca.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VotacionesUca', '0003_auto_20191119_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votacione',
            name='tipoVotacion',
            field=models.IntegerField(choices=[(0, 'SIMPLE'), (1, 'COMPLEJA')], default=VotacionesUca.models.tipoV(0)),
        ),
    ]