from django.db import models, transaction
from django.db.models import Count
from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from datetime import datetime
from django.utils import dateparse

from UsuarioUca.models import UsuarioUca


class ProcesoElectoral(models.Model):
    voto_restringido = models.BooleanField(default=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    es_consulta = models.BooleanField(default=False)


class Votacion(ProcesoElectoral):
    nombre_votacion = models.CharField(max_length=50, null=True)
    es_presencial = models.BooleanField(default=False)
    voto_rectificable = models.BooleanField(default=False)

    @property
    def espera(self):
        inicio = datetime.strptime(
            self.fecha_inicio.strftime('%Y-%m-%d') + " " + self.hora_inicio.strftime('%H:%M'),
            "%Y-%m-%d %H:%M"
        ).timestamp()

        fin = datetime.strptime(
            timezone.now().strftime('%Y-%m-%d') + " " + timezone.now().strftime('%H:%M'),
            "%Y-%m-%d %H:%M"
        ).timestamp()

        return inicio >= fin

    @property
    def votacion_cerrada(self):
        inicio = datetime.strptime(
            timezone.now().strftime('%Y-%m-%d') + " " + timezone.now().strftime('%H:%M'),
            "%Y-%m-%d %H:%M"
        ).timestamp()

        fin = datetime.strptime(
            self.fecha_fin.strftime('%Y-%m-%d') + " " + self.hora_fin.strftime('%H:%M'),
            "%Y-%m-%d %H:%M"
        ).timestamp()
        
        return fin >= inicio

    def __str__(self):
        return self.nombre_votacion


class Opcion(models.Model):
    respuesta = models.CharField(max_length=100)

    def __str__(self):
        return self.respuesta


class Pregunta(models.Model):
    TIPO_CHOICES = (
        ("0", "Simple"),
        ("1", "Compleja"),
    )

    Votacion = models.OneToOneField(Votacion, on_delete=models.CASCADE)
    tipo_votacion = models.CharField(max_length=10, choices=TIPO_CHOICES, default="Simple")
    enunciado = models.CharField(max_length=100)

    def __str__(self):
        return self.enunciado


class OpcionesCompleja(models.Model):
    Pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.CharField(max_length=100)

    def __unicode__(self):
        return self.respuesta


class UsuarioVotacion(models.Model):
    user = models.ForeignKey(UsuarioUca, on_delete=models.PROTECT, null=True)
    Votacion = models.ForeignKey(Votacion, on_delete=models.CASCADE)
    Pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    seleccion = models.CharField(max_length=100, null=True)

    def get_absolute_url(self):
        return reverse('home')

    def save(self, *args, **kwargs):
        super(UsuarioVotacion, self).save(*args, **kwargs)

        for row in UsuarioVotacion.objects.filter(user_id=self.user_id):
            if UsuarioVotacion.objects.filter(
                Votacion_id=row.Votacion_id, user=self.user_id).count() >= 2 and UsuarioVotacion.objects.filter(
                Pregunta_id=row.Pregunta_id, user=self.user_id).count() >= 2:
                row.delete()


class Eleccion(ProcesoElectoral):
    nombre = models.CharField(max_length=100)
    TIPO_ELECCION = (
        ("0", "Grupos"),
        ("1", "Unipersonales"),
    )
    tipo_eleccion = models.CharField(max_length=10, choices=TIPO_ELECCION, default="Simple")
    max_candidatos = models.IntegerField(default=2, validators=[MinValueValidator(2)])
    max_vacantes = models.FloatField(null=True, default=0.7,
                                     validators=[MinValueValidator(0.1), MaxValueValidator(0.99)])


    @property
    def espera(self):
        inicio = datetime.strptime(
            self.fecha_inicio.strftime('%Y-%m-%d') + " " + self.hora_inicio.strftime('%H:%M'),
            "%Y-%m-%d %H:%M"
        ).timestamp()

        fin = datetime.strptime(
            timezone.now().strftime('%Y-%m-%d') + " " + timezone.now().strftime('%H:%M'),
            "%Y-%m-%d %H:%M"
        ).timestamp()
        
        return inicio >= fin

    @property
    def eleccion_cerrada(self):
        inicio = datetime.strptime(
            timezone.now().strftime('%Y-%m-%d') + " " + timezone.now().strftime('%H:%M'),
            "%Y-%m-%d %H:%M"
        ).timestamp()

        fin = datetime.strptime(
            self.fecha_fin.strftime('%Y-%m-%d') + " " + self.hora_fin.strftime('%H:%M'),
            "%Y-%m-%d %H:%M"
        ).timestamp()
        
        return fin >= inicio

    def __str__(self):
        return self.nombre


class UsuarioEleccion(models.Model):
    user = models.ForeignKey(UsuarioUca, on_delete=models.DO_NOTHING, null=True)
    Eleccion = models.ForeignKey(Eleccion, on_delete=models.CASCADE)
    seleccion = models.CharField(max_length=100, null=True)

    def get_absolute_url(self):
        return reverse('home')
        

class Personas(models.Model):
    Eleccion = models.ForeignKey(Eleccion, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Censo(models.Model):
    usuario = models.ManyToManyField(UsuarioUca, blank=False)
    votacion = models.OneToOneField(Votacion, on_delete=models.CASCADE, null=True, blank=True)
    eleccion = models.OneToOneField(Eleccion, on_delete=models.CASCADE, null=True, blank=True)
