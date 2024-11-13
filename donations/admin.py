from django.contrib import admin
from .models import Causa, Donacion

class DonacionInline(admin.TabularInline): # también se podría usar StackedInline
    model = Donacion
    extra = 0  # no agregar filas vacías por defecto
    fields = ('cantidad', 'user', 'fecha_donacion')  # se podrían ajustar los campos que se muestran
    readonly_fields = ('cantidad', 'user', 'fecha_donacion')  # para que no puedan ser editados directamente desde aquí

@admin.register(Causa)
class CausaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'meta_recaudacion', 'cantidad_recaudada', 'fecha_creacion', 'fecha_fin', 'user', 'estado_meta')
    search_fields = ('titulo', 'descripcion', 'user__username')
    list_filter = ('fecha_creacion', 'fecha_fin', 'user')

    def estado_meta(self, obj):
        if obj.cantidad_recaudada >= obj.meta_recaudacion:
            return "Meta Alcanzada"
        else:
            return "Meta No Alcanzada"
    estado_meta.short_description = 'Estado de la Meta'

@admin.register(Donacion)
class DonacionAdmin(admin.ModelAdmin):
    list_display = ('causa', 'cantidad', 'fecha_donacion', 'user')
    search_fields = ('causa__titulo', 'user__username')
    list_filter = ('fecha_donacion', 'user')
    ordering = ('-fecha_donacion',)  # ordenar por fecha de donación descendente
    list_per_page = 20  # mostrar 20 donaciones por página
