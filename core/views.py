from django.shortcuts import render
from donations.models import Donacion

def home(request):
    historial_donaciones = Donacion.objects.filter(user = request.user) if request.user.is_authenticated else [] # verificar si el usuario está autenticado

    return render(request, 'core/home.html', {'historial_donaciones': historial_donaciones})
