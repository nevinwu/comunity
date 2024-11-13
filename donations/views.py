from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Causa, Donacion
from .forms import CausaForm, DonacionForm

# import stripe # librería para implementar en el futuro la pasarela de pago

# Esto permitirá implementar Stripe para la pasarela de pagos en el futuro
# stripe.api_key = settings.STRIPE_TEST_SECRET_KEY # es una key de prueba, no hay problema en hacerla pública

# Vista para listar todas las causas
def causa_list(request):
    causas = Causa.objects.all()  # obtiene todas las causas
    paginator = Paginator(causas, 6)  # agrupa causas en bloques de 6
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': request.GET.get('q', '')
    }

    return render(request, 'donations/causa_list.html', context)


# Vista de detalle de una causa específica
def causa_detail(request, causa_id):
    causa = get_object_or_404(Causa, id=causa_id)
    donaciones = causa.donaciones.all()

    # Calcula el progreso
    progress = (causa.cantidad_recaudada / causa.meta_recaudacion) * 100

    # Calcula el color en función del progreso
    if progress >= 100:
        hue_value = 120  # Verde cuando el progreso es 100% o más
    else:
        hue_value = 120 - int((progress / 100) * 120)  # Escala de gris a verde

    context = {
        'causa': causa,
        'donaciones': donaciones,
        'progress': progress,
        'hue_value': hue_value
    }

    return render(request, 'donations/causa_detail.html', context)

# Vista para crear una nueva causa
@login_required
def causa_create(request):
    if request.method == 'POST':
        form = CausaForm(request.POST)
        if form.is_valid():
            causa = form.save(commit = False)  # no guardar todavía
            causa.user = request.user  # asignar la causa al usuario autenticado
            causa.save()  # guardar la causa

            return redirect('donations:causa_list')  # redirigir a la lista de causas
    else:
        form = CausaForm()

    return render(request, 'donations/causa_form.html', {'form': form})

# Vista para eliminar una causa
@login_required
def causa_delete(request, causa_id):
    causa = get_object_or_404(Causa, id=causa_id)

    # Verificar que el usuario sea el creador o un superusuario
    if request.user == causa.user or request.user.is_superuser:
        causa.delete()
        return redirect('donations:causa_list')
    else:
        # Lanzar un error si el usuario no tiene permisos
        raise PermissionDenied("No tienes permiso para eliminar esta causa.")

# Vista para realizar una donación a una causa
@login_required
def donar(request, causa_id):
    causa = get_object_or_404(Causa, id = causa_id)

    if request.method == 'POST':
        form = DonacionForm(request.POST)
        if form.is_valid():
            # crear la donación y guardarla en la base de datos
            donacion = form.save(user = request.user, causa = causa, commit = False)
            donacion.save()

            # actualizar la cantidad recaudada de la causa
            causa.cantidad_recaudada += donacion.cantidad
            causa.save()

            # redirigir al usuario a la página de éxito
            return redirect('donations:donacion_exitoso', donacion_id = donacion.id)
    else:
        form = DonacionForm()

    return render(request, 'donations/donar.html', {
        'form': form,
        'causa': causa,
    })

# Vista cuando una donación es exitosa
def donacion_exitoso(request, donacion_id):
    donacion = get_object_or_404(Donacion, id = donacion_id)  # asegurarse de que el ID es válido
    causa = donacion.causa  # obtener la causa asociada a la donación

    return render(request, 'donations/donacion_exitoso.html', {
        'donacion': donacion,
        'causa': causa,
    })

# Vista para buscar causas del listado
def buscar_causas(request):
    query = request.GET.get('q', '')  # obtenemos el término de búsqueda
    if query:
        # Filtramos las causas que contengan el término de búsqueda en el título o en la descripción
        causas = Causa.objects.filter(
            Q(titulo__icontains=query) | Q(descripcion__icontains=query)
        )
    else:
        causas = Causa.objects.all()

    paginator = Paginator(causas, 6)  # Agrupa causas en bloques de 6
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'donations/buscar_causas.html', context)
