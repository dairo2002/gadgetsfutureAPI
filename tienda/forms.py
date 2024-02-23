from django import forms
from .models import Valoraciones

class ValoracionesForm(forms.ModelForm):
    class Meta:
        model = Valoraciones
        fields = ['comentario', 'calificacion']