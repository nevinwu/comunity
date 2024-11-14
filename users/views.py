from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from donations.models import Donacion
from .models import Profile
from .forms import UserRegisterForm, ProfileUpdateForm, CustomPasswordChangeForm

# Vista para registrar el usuario
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save() # guardar el usuario
            # comprobar si el perfil ya existe
            if not hasattr(user, 'profile'): # si no existe un perfil
                Profile.objects.create(user = user, avatar = form.cleaned_data.get('avatar'))

            # iniciar sesión automáticamente al usuario después de registrarse
            login(request, user)

            return redirect('core:home') # redirigir a la página de inico
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

# Vista para mostrar el perfil del usuario
@login_required
def profile(request):
    # obtener las donaciones del usuario
    donaciones = Donacion.objects.filter(user=request.user)

    # calcular el total donado
    total_donado = donaciones.aggregate(Sum('cantidad'))['cantidad__sum'] or 0

    # calcular el número de donaciones realizadas
    donaciones_count = donaciones.count()

    # obtener las causas donadas junto con el total donado a cada causa
    causas_donadas = donaciones.values('causa__titulo', 'causa').annotate(total_donado = Sum('cantidad')).distinct()

    # pasar los datos al template
    return render(request, 'users/profile.html', {
        'donaciones': donaciones,
        'total_donado': total_donado,
        'donaciones_count': donaciones_count,
        'causas_donadas': causas_donadas,
    })

# Vista para que el usuario actualice su perfil
@login_required
def update_profile(request):
    # obtén el perfil del usuario autenticado
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save() # guarda los cambios en el perfil
            return redirect('users:profile') # redirige al perfil después de actualizar
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'users/update_profile.html', {'form': form})

# Vista para cambiar la contraseña
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Mantener la sesión
            messages.success(request, 'Tu contraseña ha sido cambiada con éxito.')
            return redirect('users:profile')  # Redirige al perfil después de cambiar la contraseña
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})

