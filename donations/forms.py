from django import forms
from .models import Causa, Donacion
from django.utils import timezone

# Formularios utilizados en esta app
class CausaForm(forms.ModelForm):
    class Meta:
        model = Causa
        fields = ['titulo', 'descripcion', 'meta_recaudacion', 'fecha_fin']
        widgets = {
            'titulo': forms.TextInput(attrs = {'placeholder': 'Título de la causa'}),
            'descripcion': forms.Textarea(attrs = {'placeholder': 'Descripción detallada de la causa'}),
            'meta_recaudacion': forms.NumberInput(attrs = {'placeholder': 'Meta de recaudación (en euros)'}),
            'fecha_fin': forms.DateInput(attrs = {'placeholder': 'dd/mm/aaaa', 'type': 'date'}),
        }

    def clean_meta_recaudacion(self): # validación backend
        meta_recaudacion = self.cleaned_data.get('meta_recaudacion')
        if meta_recaudacion <= 0:
            raise forms.ValidationError("La meta de recaudación debe ser un número positivo.")

        return meta_recaudacion

    def clean_fecha_fin(self): # validación para la fecha de finalización
        fecha_fin = self.cleaned_data.get('fecha_fin')
        if fecha_fin <= timezone.now().date():
            raise forms.ValidationError("La fecha de finalización debe ser una fecha futura.")

        return fecha_fin

class DonacionForm(forms.ModelForm):
    class Meta:
        model = Donacion
        fields = ['cantidad']  # solo mostramos el campo 'cantidad', no 'causa'
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa la cantidad a donar'}),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise forms.ValidationError("La cantidad de la donación debe ser un valor positivo.")
        return cantidad

    def save(self, user=None, causa=None, commit=True):
        # Guardamos el objeto sin commit para asignar valores adicionales
        donacion = super().save(commit=False)

        # Asignamos el usuario y la causa, si no están presentes
        if user:
            donacion.user = user
        if causa:
            donacion.causa = causa

        if commit:
            donacion.save()

        return donacion
