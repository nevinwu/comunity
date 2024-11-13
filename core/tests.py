from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from donations.models import Donacion, Causa
from django.utils import timezone

class HomeViewTest(TestCase):

    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username = "testuser", password = "12345")

        # Crear una causa y una donación para probar el historial de donaciones
        self.causa = Causa.objects.create(
            titulo = "Causa de prueba",
            descripcion = "Descripción de prueba",
            meta_recaudacion = 1000,
            cantidad_recaudada = 0,
            fecha_fin = timezone.now().date(),
            user = self.user
        )

        self.donacion = Donacion.objects.create(
            causa = self.causa,
            cantidad = 50,
            user = self.user
        )

    def test_home_view_status_code(self):
        # Verificar que la página de inicio cargue correctamente (código 200)
        url = reverse('core:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_context_authenticated_user(self):
        # Iniciar sesión y comprobar que `historial_donaciones` esté en el contexto
        self.client.login(username = 'testuser', password = '12345')
        response = self.client.get(reverse('core:home'))

        # Comprobar que el historial de donaciones aparece en el contexto
        self.assertIn('historial_donaciones', response.context)
        # Comprobar que la donación creada está en el historial
        self.assertEqual(len(response.context['historial_donaciones']), 1)
        self.assertEqual(response.context['historial_donaciones'][0], self.donacion)

    def test_home_view_context_anonymous_user(self):
    # Comprobar que el historial de donaciones está vacío para un usuario no autenticado
        response = self.client.get(reverse('core:home'))
        self.assertIn('historial_donaciones', response.context)  # Confirma que existe
        self.assertEqual(len(response.context['historial_donaciones']), 0)  # Confirma que está vacío
