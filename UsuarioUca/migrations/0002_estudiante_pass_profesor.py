# Generated by Django 2.2 on 2019-12-17 23:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UsuarioUca', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('curso_max', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='PASS',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Pass',
            },
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('permanente', models.BooleanField(default=False)),
                ('doctor', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Profesores',
            },
        ),
    ]
