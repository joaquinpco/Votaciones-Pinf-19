# Generated by Django 2.0 on 2019-12-23 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('VotacionesUca', '0002_auto_20191223_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='censo',
            name='pregunta',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='VotacionesUca.Pregunta'),
        ),
    ]