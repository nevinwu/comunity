from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from django.db.models import Sum
from .models import Profile, Post

# Personalización para mostrar el perfil en la página del usuario en el admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'birth_date', 'created_at', 'updated_at', 'avatar_thumbnail', 'total_donado')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('total_donado',) # no permitir que se edite el total donado directamente
    exclude = ('posts',) # funcionalidad no implementada totalmente aún

    def avatar_thumbnail(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" />', obj.avatar.url)
        return "No Avatar"

    avatar_thumbnail.short_description = 'Avatar'

    def total_donado(self, obj):
        # Calcula el total donado por el usuario a todas las causas
        total = obj.user.donaciones.aggregate(Sum('cantidad'))['cantidad__sum'] or 0
        return f'{total} €'

    total_donado.short_description = 'Total Donado'

# Inline para mostrar el perfil directamente en la página de edición de usuario
class ProfileInline(admin.TabularInline): # usamos TabularInline para hacerlo más compacto
    model = Profile
    extra = 0 # no agregar filas vacías por defecto
    fields = ('bio', 'location', 'birth_date', 'avatar', 'total_donado')
    readonly_fields = ('total_donado',) # no permitir que se edite el total donado directamente
    can_delete = False  # para evitar eliminar el perfil desde aquí

    def total_donado(self, obj):
        total = obj.user.donaciones.aggregate(Sum('cantidad'))['cantidad__sum'] or 0
        return f'{total} €'
    total_donado.short_description = 'Total Donado'

# Personalización del modelo User para incluir el perfil en el admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'profile_total_donado')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')

    # Mostramos el perfil directamente en la página del usuario en el admin
    inlines = [ProfileInline]

    def profile_total_donado(self, obj):
        # Calculamos el total donado desde el perfil del usuario
        profile = obj.profile
        total = profile.user.donaciones.aggregate(Sum('cantidad'))['cantidad__sum'] or 0
        return f'{total} €'
    profile_total_donado.short_description = 'Total Donado'

# Re-registrar el modelo User para incluir el perfil
admin.site.unregister(User) # desregistrar el modelo User por defecto
admin.site.register(User, UserAdmin) # re-registrar el modelo User con las personalizaciones
admin.site.register(Profile, ProfileAdmin) # registrar el modelo Profile con las mejoras
admin.site.unregister(User) # desregistrar el modelo User por defecto
admin.site.unregister(Group) # desregistrar el modelo Group por defecto

# Personalización para el modelo Post, no está terminado de implementar pero lo dejo listo
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at',)
admin.site.register(Post, PostAdmin)
