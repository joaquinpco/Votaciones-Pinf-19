# Generated by Django 2.2 on 2020-01-16 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('VotacionesUca', '0004_auto_20200114_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariovotacion',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
