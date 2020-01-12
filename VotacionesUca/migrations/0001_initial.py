# Generated by Django 2.0 on 2020-01-12 00:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Censo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Opcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='OpcionesCompleja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Personas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_votacion', models.CharField(choices=[('0', 'Simple'), ('1', 'Compleja')], default='Simple', max_length=10)),
                ('enunciado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ProcesoElectoral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voto_restringido', models.BooleanField(default=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('es_consulta', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioEleccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seleccion', models.CharField(max_length=20, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioVotacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seleccion', models.CharField(max_length=20, null=True)),
                ('Pregunta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='VotacionesUca.Pregunta')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Eleccion',
            fields=[
                ('procesoelectoral_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='VotacionesUca.ProcesoElectoral')),
                ('nombre', models.CharField(max_length=50)),
                ('tipo_eleccion', models.CharField(choices=[('0', 'Grupos'), ('1', 'Unipersonales')], default='Simple', max_length=10)),
                ('max_candidatos', models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(2)])),
                ('max_vacantes', models.FloatField(default=0.7, null=True, validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(0.99)])),
            ],
            bases=('VotacionesUca.procesoelectoral',),
        ),
        migrations.CreateModel(
            name='Votacion',
            fields=[
                ('procesoelectoral_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='VotacionesUca.ProcesoElectoral')),
                ('nombre_votacion', models.CharField(max_length=50, null=True)),
                ('es_presencial', models.BooleanField(default=False)),
                ('voto_rectificable', models.BooleanField(default=False)),
            ],
            bases=('VotacionesUca.procesoelectoral',),
        ),
        migrations.AddField(
            model_name='opcionescompleja',
            name='Pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VotacionesUca.Pregunta'),
        ),
        migrations.AddField(
            model_name='usuariovotacion',
            name='Votacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='VotacionesUca.Votacion'),
        ),
        migrations.AddField(
            model_name='usuarioeleccion',
            name='Eleccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='VotacionesUca.Eleccion'),
        ),
        migrations.AddField(
            model_name='pregunta',
            name='Votacion',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='VotacionesUca.Votacion'),
        ),
        migrations.AddField(
            model_name='personas',
            name='Eleccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VotacionesUca.Eleccion'),
        ),
        migrations.AddField(
            model_name='censo',
            name='eleccion',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='VotacionesUca.Eleccion'),
        ),
        migrations.AddField(
            model_name='censo',
            name='votacion',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='VotacionesUca.Votacion'),
        ),
    ]
