# users/forms.py
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone
from datetime import datetime
from .models import ProcesoElectoral, Pregunta, Votacion, Eleccion,  Censo, UsuarioVotacion
from bootstrap_modal_forms.forms import BSModalForm


# c=[('0','Simple'),('1','Compleja')]
# b=[('0','No'),('1','Sí')]

class ProcesoElectoralForm(forms.ModelForm):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control inputstl', 'placeholder': 'Select Date'},
                               format='%Y/%m/%d'))
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control inputstl', 'placeholder': 'Select Date'},
                               format='%Y/%m/%d'))
    # hora_inicio = forms.TimeField()
    # hora_fin = forms.TimeField()
    es_consulta = forms.BooleanField(required=False)
    hora_inicio = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control inputstl'}))
    hora_fin = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control inputstl'}))

    # esConsulta=forms.ChoiceField(widget=forms.Select(), choices=b)
    # fecha_inicio = forms.DateField()
    # fecha_fin = forms.DateField()
    # nombreFicheroCenso=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Nombre del Censo'}),required=True)

    class Meta:
        model = ProcesoElectoral
        fields = '__all__'


# class OpcionesSimpleForm(forms.ModelForm):
#     pass


# class OpcionesComplejaForm(forms.ModelForm):
#     Respuesta_elegida = forms.MultipleChoiceField(choices=[], label='Respuestas', required=False,
#                                                   widget=forms.SelectMultiple(
#                                                       attrs={
#                                                           'class': 'form-control'
#                                                       }
#                                                   ))
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         unique_respuestas = OpcionesCompleja.objects.order_by('respuesta').values_list('respuesta',
#                                                                                        flat=True).distinct()
#         self.fields['Respuesta_elegida'].choices = [(respuesta, respuesta) for respuesta in unique_respuestas]
#
#     class Meta:
#         model = OpcionesCompleja
#         fields = '__all__'


class VotacionForm(ProcesoElectoralForm):
    voto_restringido = forms.BooleanField(required=False)
    nombre_votacion = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la votacion'}), required=True)
    es_presencial = forms.BooleanField(required=False)
    voto_rectificable = forms.BooleanField(required=False)

    class Meta:
        model = Votacion
        fields = '__all__'

    def clean(self):
        inicio = self.cleaned_data['fecha_inicio']
        fin = self.cleaned_data['fecha_fin']

        if inicio.strftime('%Y-%m-%d') <= datetime.now().strftime('%Y-%m-%d'):
            raise ValidationError('La fecha ser mayor que la actual.')

        if inicio.strftime('%Y-%m-%d') >= fin.strftime('%Y-%m-%d'):
            raise ValidationError('La fecha de Fin debe ser mayor a la de Inicio.')

        return self.cleaned_data


class createCensoForm(ModelForm):
    class Meta:
        model = Censo
        fields = '__all__'
        labels = {'usuario': ('Usuarios pertenecientes al censo'), 'pregunta': ('Pregunta'), }
        help_texts = {'usuario': (
            'Elige los usuarios que pertenecen al censo. Recuerda que serán los usuarios que tendrán acceso a la votación'),
            'pregunta': ('Elige la pregunta a la que hace referencia el censo'),
        }

        widgets = {'usuario': forms.SelectMultiple(attrs={'class': 'form-control'}),
                   'pregunta': forms.Select(attrs={'class': 'form-control'}),
                   }


class realizarVotacionForm(ModelForm):

    # usuario = models.ForeignKey("auth.User", blank=True)
    class Meta:
        model = UsuarioVotacion
        fields = 'Votacion', 'Pregunta', 'seleccion'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Pregunta'].queryset = Pregunta.objects.none()

        if 'Votacion' in self.data:
            try:
                Votacion_id = int(self.data.get('Votacion'))
                self.fields['Pregunta'].queryset = Pregunta.objects.filter(Votacion_id=Votacion_id).order_by('enunciado')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['Pregunta'].queryset = self.instance.Votacion.Pregunta_set.order_by('enunciado')





class PreguntaForm(BSModalForm):
    class Meta:
        model = Pregunta
        fields = '__all__'


class PreguntaFormVotacion(ModelForm):
    class Meta:
        model = Pregunta
        fields = '__all__'
