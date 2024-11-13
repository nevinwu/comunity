from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Causa, Donacion
from .forms import CausaForm, DonacionForm
from datetime import date, timedelta

# Pruebas para la app donations

# Pruebas de modelos
class CausaModelTest(TestCase):
    def test_causa_creation(self):
        user = User.objects.create_user(username='testuser')
        causa = Causa.objects.create(
            titulo='Ayuda Escolar',
            descripcion='Apoyo para estudiantes',
            meta_recaudacion=500.00,
            user=user,
            fecha_fin=date.today() + timedelta(days=10)
        )
        self.assertEqual(str(causa), 'Ayuda Escolar')

class DonacionModelTest(TestCase):
    def test_donacion_creation(self):
        user = User.objects.create_user(username='testuser')
        causa = Causa.objects.create(
            titulo='Ayuda Escolar',
            descripcion='Apoyo para estudiantes',
            meta_recaudacion=500.00,
            user=user,
            fecha_fin=date.today() + timedelta(days=10)
        )
        donacion = Donacion.objects.create(
            causa=causa,
            cantidad=50.00,
            user=user
        )
        self.assertEqual(str(donacion), f"Donación de {donacion.cantidad} a {causa.titulo} por {user.username}")

# Pruebas de formularios
class CausaFormTest(TestCase):
    def test_causa_form_valid(self):
        form_data = {
            'titulo': 'Apoyo Comunitario',
            'descripcion': 'Descripción de la causa',
            'meta_recaudacion': 1000.00,
            'fecha_fin': date.today() + timedelta(days=5)
        }
        form = CausaForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_causa_form_invalid(self):
        form_data = {
            'titulo': '',
            'descripcion': 'Descripción de la causa',
            'meta_recaudacion': 1000.00,
            'fecha_fin': date.today() - timedelta(days=1)  # Fecha de fin pasada
        }
        form = CausaForm(data=form_data)
        self.assertFalse(form.is_valid())

class DonacionFormTest(TestCase):
    def test_donacion_form_valid(self):
        form_data = {
            'cantidad': 50.00
        }
        form = DonacionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_donacion_form_invalid(self):
        form_data = {
            'cantidad': -10.00
        }
        form = DonacionForm(data=form_data)
        self.assertFalse(form.is_valid())

# Pruebas de vistas
class CausaViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.causa = Causa.objects.create(
            titulo='Ayuda Escolar',
            descripcion='Apoyo para estudiantes',
            meta_recaudacion=500.00,
            user=self.user,
            fecha_fin=date.today() + timedelta(days=10)
        )

    def test_causa_list_view(self):
        response = self.client.get(reverse('donations:causa_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.causa.titulo)

    def test_causa_detail_view(self):
        response = self.client.get(reverse('donations:causa_detail', args=[self.causa.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.causa.descripcion)

    def test_causa_create_view(self):
        response = self.client.get(reverse('donations:causa_create'))
        self.assertEqual(response.status_code, 200)

    def test_causa_delete_view(self):
        response = self.client.post(reverse('donations:causa_delete', args=[self.causa.id]))
        self.assertRedirects(response, reverse('donations:causa_list'))
        self.assertFalse(Causa.objects.filter(id=self.causa.id).exists())

    def test_donar_view(self):
        response = self.client.get(reverse('donations:donar', args=[self.causa.id]))
        self.assertEqual(response.status_code, 200)

    def test_buscar_causas_view(self):
        response = self.client.get(reverse('donations:buscar_causas') + '?q=escolar')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.causa.titulo)

# Pruebas de permisos
class CausaPermissionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.other_user = User.objects.create_user(username='otheruser', password='12345')
        self.causa = Causa.objects.create(
            titulo='Ayuda Escolar',
            descripcion='Apoyo para estudiantes',
            meta_recaudacion=500.00,
            user=self.user,
            fecha_fin=date.today() + timedelta(days=10)
        )

    def test_causa_delete_permission(self):
        self.client.login(username='otheruser', password='12345')
        response = self.client.post(reverse('donations:causa_delete', args=[self.causa.id]))
        self.assertEqual(response.status_code, 403)  # Permission denied

    def test_causa_delete_permission_creator(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('donations:causa_delete', args=[self.causa.id]))
        self.assertRedirects(response, reverse('donations:causa_list'))
        self.assertFalse(Causa.objects.filter(id=self.causa.id).exists())
